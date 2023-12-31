"""Init database.

Revision ID: 3f31d0b47070
Revises: 
Create Date: 2023-07-23 01:16:12.929611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3f31d0b47070"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "invitation_code",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("storage_size", sa.Integer(), nullable=False, default=1024),
        sa.Column("expired_at", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("storage_size", sa.Integer(), nullable=False, default=1024),
        sa.Column("last_seen", sa.Float(), nullable=False, default=0.0),
        sa.Column("login_counter", sa.Integer(), nullable=False, default=0),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "file",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("download_cnt", sa.Integer(), nullable=False, default=0),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "shared_file",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("file_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["file_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("file_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("shared_file")
    op.drop_table("file")
    op.drop_table("user")
    op.drop_table("invitation_code")
    # ### end Alembic commands ###
