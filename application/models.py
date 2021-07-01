import sqlalchemy as sa

metadata = sa.MetaData()

devices = sa.Table(
    'devices',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('dev_id', sa.String(length=200), nullable=False),
    sa.Column('dev_type', sa.VARCHAR(length=120), nullable=False),
    sa.Index('devices_dev_id_dev_type_index', 'dev_id', 'dev_type')
)

endpoints = sa.Table(
    'endpoints',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('device_id', sa.BigInteger, sa.ForeignKey(
        'devices.id',
        onupdate='CASCADE',
        ondelete='CASCADE'
    ),
              nullable=False),
    sa.Column('text', sa.String)
)
