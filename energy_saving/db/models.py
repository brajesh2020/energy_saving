"""Database model"""
import logging
from oslo_utils import uuidutils
import simplejson as json

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy import String


BASE = declarative_base()
logger = logging.getLogger(__name__)
COLUMN_TYPE_CONVERTER = {
    dict: json.loads
}


def convert_column_value(value, value_type):
    try:
        if value_type in COLUMN_TYPE_CONVERTER:
            return COLUMN_TYPE_CONVERTER[value_type](value)
        return value_type(value)
    except Exception as error:
        logger.exception(error)
        logger.error(
            'failed to convert %s to %s: %s',
            value, value_type, error
        )
        raise error


class LocationMixin(object):
    location = Column(JSON)


class AttrMixin(object):
    type = Column(
        Enum('binary', 'continuous', 'integer', 'discrete'),
        default='continuous', server_default='continuous'
    )
    unit = Column(String(36))
    mean = Column(Float())
    deviation = Column(Float())
    max = Column(Float())
    min = Column(Float())
    differentiation_mean = Column(Float())
    differentiation_deviation = Column(Float())
    differentiation_max = Column(Float())
    differentiation_min = Column(Float())
    possible_values = Column(JSON)
    measurement_pattern = Column(String(256))


class ParamMixin(object):
    type = Column(
        Enum('binary', 'continuous', 'integer', 'discrete'),
        default='continuous', server_default='continuous'
    )
    unit = Column(String(36))
    max = Column(Float())
    min = Column(Float())
    possible_values = Column(JSON)


class Datacenter(BASE, LocationMixin):
    """Datacenter table."""
    __tablename__ = 'datacenter'
    name = Column(
        String(36), primary_key=True
    )
    type = Column(
        Enum('production', 'lab'), default='produdction',
        server_default='production'
    )
    properties = Column(JSON)
    models = Column(JSON)
    time_interval = Column(Integer)
    sensors = relationship(
        'Sensor',
        foreign_keys='[Sensor.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    sensor_attributes = relationship(
        'SensorAttr',
        foreign_keys='[SensorAttr.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    controllers = relationship(
        'Controller',
        foreign_keys='[Controller.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    controller_attributes = relationship(
        'ControllerAttr',
        foreign_keys='[ControllerAttr.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    controller_parameters = relationship(
        'ControllerParam',
        foreign_keys='[ControllerParam.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    environment_sensors = relationship(
        'EnvironmentSensor',
        foreign_keys='[EnvironmentSensor.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    environment_sensor_attributes = relationship(
        'EnvironmentSensorAttr',
        foreign_keys='[EnvironmentSensorAttr.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    power_supplies = relationship(
        'PowerSupply',
        foreign_keys='[PowerSupply.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    power_supply_attributes = relationship(
        'PowerSupplyAttr',
        foreign_keys='[PowerSupplyAttr.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    controller_power_supplies = relationship(
        'ControllerPowerSupply',
        foreign_keys='[ControllerPowerSupply.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    controller_power_supply_attributes = relationship(
        'ControllerPowerSupplyAttr',
        foreign_keys='[ControllerPowerSupplyAttr.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )
    test_results = relationship(
        'TestResult',
        foreign_keys='[TestResult.datacenter_name]',
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('datacenter', viewonly=True)
    )

    def __str__(self):
        return 'Datacenter{name=%s}' % self.name


class PowerSupply(BASE, LocationMixin):
    """power supply table."""
    __tablename__ = 'power_supply'
    datacenter_name = Column(
        String(36),
        ForeignKey(
            'datacenter.name',
            onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    attribute_data = relationship(
        'PowerSupplyAttrData',
        foreign_keys=(
            '[PowerSupplyAttrData.datacenter_name,'
            'PowerSupplyAttrData.power_supply_name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('power_supply', viewonly=True)
    )

    def __str__(self):
        return 'PowerSupply[datacenter_name=%s,name=%s]' % (
            self.datacenter_name, self.name
        )


class PowerSupplyAttr(BASE, AttrMixin):
    """power supply attribute table."""
    __tablename__ = 'power_supply_attribute'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    attribute_data = relationship(
        'PowerSupplyAttrData',
        foreign_keys=(
            '[PowerSupplyAttrData.datacenter_name,'
            'PowerSupplyAttrData.name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('attribute', viewonly=True)
    )

    def __str__(self):
        return 'PowerSupplyAttr[datacenter_name=%s,name=%s]' % (
            self.datacenter_name, self.name
        )


class PowerSupplyAttrData(BASE):
    """power supply attribute data table."""
    __tablename__ = 'power_supply_attribute_data'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    power_supply_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'name'],
            [
                'power_supply_attribute.datacenter_name',
                'power_supply_attribute.name'
            ],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'power_supply_name'],
            ['power_supply.datacenter_name', 'power_supply.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        )
    )

    def __str__(self):
        return (
            'PowerSupplyAttrData[datacenter_name=%s,'
            'power_supply_name=%s,name=%s]'
        ) % (
            self.datacenter_name, self.power_supply_name, self.name
        )


class ControllerPowerSupply(BASE, LocationMixin):
    """controller power supply table."""
    __tablename__ = 'controller_power_supply'
    datacenter_name = Column(
        String(36),
        ForeignKey(
            'datacenter.name',
            onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    attribute_data = relationship(
        'ControllerPowerSupplyAttrData',
        foreign_keys=(
            '[ControllerPowerSupplyAttrData.datacenter_name,'
            'ControllerPowerSupplyAttrData.controller_power_supply_name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('controller_power_supply', viewonly=True)
    )

    def __str__(self):
        return 'ControllerPowerSupply[datacenter_name=%s,name=%s]' % (
            self.datacenter_name, self.name
        )


class ControllerPowerSupplyAttr(BASE, AttrMixin):
    """power supply attribute table."""
    __tablename__ = 'controller_power_supply_attribute'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    attribute_data = relationship(
        'ControllerPowerSupplyAttrData',
        foreign_keys=(
            '[ControllerPowerSupplyAttrData.datacenter_name,'
            'ControllerPowerSupplyAttrData.name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('attribute', viewonly=True)
    )

    def __str__(self):
        return 'ControllerPowerSupplyAttr[datacenter_name=%s,name=%s]' % (
            self.datacenter_name, self.name
        )


class ControllerPowerSupplyAttrData(BASE):
    """controller power supply attribute data table."""
    __tablename__ = 'controller_power_supply_attribute_data'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    controller_power_supply_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'name'],
            [
                'controller_power_supply_attribute.datacenter_name',
                'controller_power_supply_attribute.name'
            ],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'controller_power_supply_name'],
            [
                'controller_power_supply.datacenter_name',
                'controller_power_supply.name'
            ],
            onupdate="CASCADE", ondelete="CASCADE"
        )
    )

    def __str__(self):
        return (
            'ControllerPowerSupplyAttrData[datacenter_name=%s,'
            'controller_power_supply_name=%s,name=%s]'
        ) % (
            self.datacenter_name, self.controller_power_supply_name,
            self.name
        )


class Sensor(BASE, LocationMixin):
    """Sensor table."""
    __tablename__ = 'sensor'
    datacenter_name = Column(
        String(36),
        ForeignKey(
            'datacenter.name',
            onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    attribute_data = relationship(
        'SensorAttrData',
        foreign_keys=(
            '[SensorAttrData.datacenter_name,'
            'SensorAttrData.sensor_name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('sensor', viewonly=True)
    )

    def __str__(self):
        return 'Sensor[datacenter_name=%s,name=%s]' % (
            self.datacenter_name, self.name
        )


class SensorAttr(BASE, AttrMixin):
    """Sensor attribute table."""
    __tablename__ = 'sensor_attribute'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    attribute_data = relationship(
        'SensorAttrData',
        foreign_keys=(
            '[SensorAttrData.datacenter_name,'
            'SensorAttrData.name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('attribute', viewonly=True)
    )
    slo = relationship(
        'SensorAttrSLO',
        foreign_keys=(
            '[SensorAttrSLO.datacenter_name,'
            'SensorAttrSLO.sensor_attribute_name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('attribute', viewonly=True)
    )

    def __str__(self):
        return 'SensorAttr[datacenter_name=%s,name=%s]' % (
            self.datacenter_name, self.name
        )


class SensorAttrSLO(BASE):
    """Sensor attribute slo."""
    __tablename__ = 'sensor_attribute_slo'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    sensor_attribute_name = Column(String(36), primary_key=True)
    min_threshold = Column(Float())
    max_threshold = Column(Float())
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'sensor_attribute_name'],
            ['sensor_attribute.datacenter_name', 'sensor_attribute.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        )
    )

    def __str__(self):
        return 'SensorAttrSLO[datacenter_name=%s,sensor_attribute_name=%s]' % (
            self.datacenter_name, self.sensor_attribute_name
        )


class SensorAttrData(BASE):
    """Sensor attribute data table."""
    __tablename__ = 'sensor_attribute_data'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    sensor_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'name'],
            [
                'sensor_attribute.datacenter_name',
                'sensor_attribute.name'
            ],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'sensor_name'],
            ['sensor.datacenter_name', 'sensor.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        )
    )

    def __str__(self):
        return (
            'SensorAttrData[datacenter_name=%s,'
            'sensor_name=%s,name=%s]'
        ) % (
            self.datacenter_name, self.sensor_name, self.name
        )


class Controller(BASE, LocationMixin):
    """controller table."""
    __tablename__ = 'controller'
    datacenter_name = Column(
        String(36),
        ForeignKey('datacenter.name', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    attribute_data = relationship(
        'ControllerAttrData',
        foreign_keys=(
            '[ControllerAttrData.datacenter_name,'
            'ControllerAttrData.controller_name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('controller', viewonly=True)
    )
    parameter_data = relationship(
        'ControllerParamData',
        foreign_keys=(
            '[ControllerParamData.datacenter_name,'
            'ControllerParamData.controller_name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('controller', viewonly=True)
    )

    def __str__(self):
        return 'Controller[datacenter_name=%s,name=%s]' % (
            self.datacenter_name, self.name
        )


class ControllerAttr(BASE, AttrMixin):
    """controller attribute table."""
    __tablename__ = 'controller_attribute'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    attribute_data = relationship(
        'ControllerAttrData',
        foreign_keys=(
            '[ControllerAttrData.datacenter_name,'
            'ControllerAttrData.name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('attribute', viewonly=True)
    )

    def __str__(self):
        return (
            'ControllerAttr[datacenter_name=%s,name=%s]'
        ) % (
            self.datacenter_name, self.name
        )


class ControllerAttrData(BASE):
    """controller attribute data table."""
    __tablename__ = 'controller_attribute_data'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    controller_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'name'],
            [
                'controller_attribute.datacenter_name',
                'controller_attribute.name'
            ],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'controller_name'],
            ['controller.datacenter_name', 'controller.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        )
    )

    def __str__(self):
        return (
            'ControllerAttrData[datacenter_name=%s,'
            'controller_name=%s,name=%s]'
        ) % (
            self.datacenter_name, self.controller_name, self.name
        )


class ControllerParam(BASE, ParamMixin):
    """controller param table."""
    __tablename__ = 'controller_parameter'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    parameter_data = relationship(
        'ControllerParamData',
        foreign_keys=(
            '[ControllerParamData.datacenter_name,'
            'ControllerParamData.name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('parameter', viewonly=True)
    )

    def __str__(self):
        return (
            'ControllerParam[datacenter_name=%s,'
            'name=%s]'
        ) % (
            self.datacenter_name, self.name
        )


class ControllerParamData(BASE):
    """controller param data table."""
    __tablename__ = 'controller_parameter_data'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    controller_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'name'],
            [
                'controller_parameter.datacenter_name',
                'controller_parameter.name'
            ],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'controller_name'],
            ['controller.datacenter_name', 'controller.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        )
    )

    def __str__(self):
        return (
            'ControllerParamData[datacenter_name=%s,'
            'controller_name=%s,name=%s]'
        ) % (
            self.datacenter_name, self.controller_name, self.name
        )


class EnvironmentSensor(BASE, LocationMixin):
    """Environment sensor table."""
    __tablename__ = 'environment_sensor'
    datacenter_name = Column(
        String(36),
        ForeignKey('datacenter.name', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    attribute_data = relationship(
        'EnvironmentSensorAttrData',
        foreign_keys=(
            '[EnvironmentSensorAttrData.datacenter_name,'
            'EnvironmentSensorAttrData.environment_sensor_name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('environment_sensor', viewonly=True)
    )

    def __str__(self):
        return 'EnvironmentSensor[datacenter_name=%s,name=%s]' % (
            self.datacenter_name, self.name
        )


class EnvironmentSensorAttr(BASE, AttrMixin):
    """Environment sensor attribute table."""
    __tablename__ = 'environment_sensor_attribute'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    properties = Column(JSON)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
    )
    attribute_data = relationship(
        'EnvironmentSensorAttrData',
        foreign_keys=(
            '[EnvironmentSensorAttrData.datacenter_name,'
            'EnvironmentSensorAttrData.name]'
        ),
        passive_deletes=True,
        cascade='all, delete-orphan',
        backref=backref('environment_sensor_attribute', viewonly=True)
    )

    def __str__(self):
        return (
            'EnvironmentSensorAttr[datacenter_name=%s,'
            'name=%s]'
        ) % (
            self.datacenter_name, self.name
        )


class EnvironmentSensorAttrData(BASE):
    """Environment sensor attribute data table."""
    __tablename__ = 'environment_sensor_attribute_data'
    datacenter_name = Column(
        String(36),
        primary_key=True
    )
    environment_sensor_name = Column(
        String(36),
        primary_key=True
    )
    name = Column(String(36), primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['datacenter_name'],
            ['datacenter.name'],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'name'],
            [
                'environment_sensor_attribute.datacenter_name',
                'environment_sensor_attribute.name'
            ],
            onupdate="CASCADE", ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ['datacenter_name', 'environment_sensor_name'],
            [
                'environment_sensor.datacenter_name',
                'environment_sensor.name'
            ],
            onupdate="CASCADE", ondelete="CASCADE"
        )
    )

    def __str__(self):
        return (
            'EnvironmentSensorAttrData[datacenter_name=%s,'
            'environment_sensor_name=%s,name=%s]'
        ) % (
            self.datacenter_name, self.environment_sensor_name, self.name
        )


class TestResult(BASE):
    """TestResult table."""
    __tablename__ = 'test_result'
    datacenter_name = Column(
        String(36),
        ForeignKey('datacenter.name', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
    name = Column(
        String(36),
        primary_key=True,
        default=uuidutils.generate_uuid
    )
    properties = Column(JSON)
    status = Column(
        Enum('initialized', 'pending', 'success', 'failure'),
        default='initialized', server_default='initialized'
    )

    def __str__(self):
        return 'TestResult[datacenter_name=%s,name=%s,status=%s]' % (
            self.datacenter_name, self.name, self.status
        )
