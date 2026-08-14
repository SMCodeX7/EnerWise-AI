"""create profiles and assessments

Revision ID: 44c9bc3e203b
Revises:
Create Date: 2026-08-14 16:36:05.106283

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "44c9bc3e203b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role_enum = postgresql.ENUM(
    "USER",
    "ADMIN",
    name="user_role",
    schema="public",
    create_type=False,
)

assessment_status_enum = postgresql.ENUM(
    "DRAFT",
    "PROCESSING",
    "COMPLETED",
    "FAILED",
    name="assessment_status",
    schema="public",
    create_type=False,
)


def upgrade() -> None:
    """Create the initial EnerWise application schema."""

    bind = op.get_bind()

    # ------------------------------------------------------------------
    # PostgreSQL enum types
    # ------------------------------------------------------------------

    user_role_enum.create(bind, checkfirst=True)
    assessment_status_enum.create(bind, checkfirst=True)

    # ------------------------------------------------------------------
    # Profiles
    # ------------------------------------------------------------------

    op.create_table(
        "profiles",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "full_name",
            sa.String(length=150),
            nullable=True,
        ),
        sa.Column(
            "role",
            user_role_enum,
            server_default="USER",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["auth.users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )

    # ------------------------------------------------------------------
    # Assessments
    # ------------------------------------------------------------------

    op.create_table(
        "assessments",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=200),
            nullable=True,
        ),
        sa.Column(
            "input_text",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "energy_profile",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "status",
            assessment_status_enum,
            server_default="DRAFT",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["public.profiles.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )

    op.create_index(
        op.f("ix_public_assessments_user_id"),
        "assessments",
        ["user_id"],
        unique=False,
        schema="public",
    )

    # ------------------------------------------------------------------
    # Keep updated_at correct even when updates come through Supabase
    # rather than SQLAlchemy.
    # ------------------------------------------------------------------

    op.execute(
        """
        CREATE OR REPLACE FUNCTION public.enerwise_set_updated_at()
        RETURNS trigger
        LANGUAGE plpgsql
        SET search_path = ''
        AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$;
        """
    )

    op.execute(
        """
        CREATE TRIGGER enerwise_profiles_set_updated_at
        BEFORE UPDATE ON public.profiles
        FOR EACH ROW
        EXECUTE FUNCTION public.enerwise_set_updated_at();
        """
    )

    op.execute(
        """
        CREATE TRIGGER enerwise_assessments_set_updated_at
        BEFORE UPDATE ON public.assessments
        FOR EACH ROW
        EXECUTE FUNCTION public.enerwise_set_updated_at();
        """
    )

    # ------------------------------------------------------------------
    # Automatically create an EnerWise profile when Supabase creates
    # an authenticated user.
    # ------------------------------------------------------------------

    op.execute(
        """
        CREATE OR REPLACE FUNCTION public.enerwise_handle_new_user()
        RETURNS trigger
        LANGUAGE plpgsql
        SECURITY DEFINER
        SET search_path = ''
        AS $$
        BEGIN
            INSERT INTO public.profiles (
                id,
                full_name
            )
            VALUES (
                NEW.id,
                NEW.raw_user_meta_data ->> 'full_name'
            );

            RETURN NEW;
        END;
        $$;
        """
    )

    op.execute(
        """
        CREATE TRIGGER enerwise_on_auth_user_created
        AFTER INSERT ON auth.users
        FOR EACH ROW
        EXECUTE FUNCTION public.enerwise_handle_new_user();
        """
    )

    # ------------------------------------------------------------------
    # Row Level Security
    # ------------------------------------------------------------------

    op.execute(
        """
        ALTER TABLE public.profiles
        ENABLE ROW LEVEL SECURITY;
        """
    )

    op.execute(
        """
        ALTER TABLE public.assessments
        ENABLE ROW LEVEL SECURITY;
        """
    )

    # ------------------------------------------------------------------
    # Privileges
    #
    # Normal users may update full_name but NOT role.
    # Therefore a user cannot promote themselves from USER to ADMIN.
    # ------------------------------------------------------------------

    op.execute(
        """
        REVOKE ALL ON TABLE public.profiles
        FROM anon, authenticated;
        """
    )

    op.execute(
        """
        GRANT SELECT ON TABLE public.profiles
        TO authenticated;
        """
    )

    op.execute(
        """
        GRANT UPDATE (full_name) ON TABLE public.profiles
        TO authenticated;
        """
    )

    op.execute(
        """
        REVOKE ALL ON TABLE public.assessments
        FROM anon, authenticated;
        """
    )

    op.execute(
        """
        GRANT SELECT, INSERT, UPDATE, DELETE
        ON TABLE public.assessments
        TO authenticated;
        """
    )

    # ------------------------------------------------------------------
    # Profile policies
    # ------------------------------------------------------------------

    op.execute(
        """
        CREATE POLICY "profiles_select_own"
        ON public.profiles
        FOR SELECT
        TO authenticated
        USING (
            (SELECT auth.uid()) = id
        );
        """
    )

    op.execute(
        """
        CREATE POLICY "profiles_update_own"
        ON public.profiles
        FOR UPDATE
        TO authenticated
        USING (
            (SELECT auth.uid()) = id
        )
        WITH CHECK (
            (SELECT auth.uid()) = id
        );
        """
    )

    # ------------------------------------------------------------------
    # Assessment policies
    # ------------------------------------------------------------------

    op.execute(
        """
        CREATE POLICY "assessments_select_own"
        ON public.assessments
        FOR SELECT
        TO authenticated
        USING (
            (SELECT auth.uid()) = user_id
        );
        """
    )

    op.execute(
        """
        CREATE POLICY "assessments_insert_own"
        ON public.assessments
        FOR INSERT
        TO authenticated
        WITH CHECK (
            (SELECT auth.uid()) = user_id
        );
        """
    )

    op.execute(
        """
        CREATE POLICY "assessments_update_own"
        ON public.assessments
        FOR UPDATE
        TO authenticated
        USING (
            (SELECT auth.uid()) = user_id
        )
        WITH CHECK (
            (SELECT auth.uid()) = user_id
        );
        """
    )

    op.execute(
        """
        CREATE POLICY "assessments_delete_own"
        ON public.assessments
        FOR DELETE
        TO authenticated
        USING (
            (SELECT auth.uid()) = user_id
        );
        """
    )


def downgrade() -> None:
    """Remove the initial EnerWise application schema."""

    bind = op.get_bind()

    # Remove trigger from Supabase-owned auth.users first.
    op.execute(
        """
        DROP TRIGGER IF EXISTS enerwise_on_auth_user_created
        ON auth.users;
        """
    )

    op.execute(
        """
        DROP FUNCTION IF EXISTS public.enerwise_handle_new_user();
        """
    )

    # Policies
    op.execute(
        """
        DROP POLICY IF EXISTS "assessments_delete_own"
        ON public.assessments;
        """
    )

    op.execute(
        """
        DROP POLICY IF EXISTS "assessments_update_own"
        ON public.assessments;
        """
    )

    op.execute(
        """
        DROP POLICY IF EXISTS "assessments_insert_own"
        ON public.assessments;
        """
    )

    op.execute(
        """
        DROP POLICY IF EXISTS "assessments_select_own"
        ON public.assessments;
        """
    )

    op.execute(
        """
        DROP POLICY IF EXISTS "profiles_update_own"
        ON public.profiles;
        """
    )

    op.execute(
        """
        DROP POLICY IF EXISTS "profiles_select_own"
        ON public.profiles;
        """
    )

    # Tables
    op.drop_index(
        op.f("ix_public_assessments_user_id"),
        table_name="assessments",
        schema="public",
    )

    op.drop_table(
        "assessments",
        schema="public",
    )

    op.drop_table(
        "profiles",
        schema="public",
    )

    # updated_at function is no longer referenced after dropping tables.
    op.execute(
        """
        DROP FUNCTION IF EXISTS public.enerwise_set_updated_at();
        """
    )

    # PostgreSQL ENUMs are separate database objects.
    assessment_status_enum.drop(bind, checkfirst=True)
    user_role_enum.drop(bind, checkfirst=True)