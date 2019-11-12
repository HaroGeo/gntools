# coding: utf-8
#
# Copyright 2019 Geocom Informatik AG / VertiGIS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
The definitions module provides access to object names within the GEONIS data model (e.g. tables, fields etc.).
The data model uses German names by default, but a user can override these names using a definition table,
which is stored in the geodatabase as GN<solution>_DEFINITION (e.g. GNELE_DEFINITION).

The :class:`DefinitionTable` class reads all key-value pairs from the definition table in the database.
If no match with a certain key has been found, the default German object name is returned.

The default German names and the mappings to their English counterparts are defined in the classes in this module.

The :class:`RelationTable` class reads the inter-table-relationships from the GNREL_DEFINITION table in the geodatabase.
"""

from warnings import warn as _warn

from gntools.common import const as _const
from gntools.common import i18n as _i18n
from gpf import lookups as _lookups
from gpf import paths as _paths
from gpf.common import validate as _vld
from gpf.common import textutils as _tu
from gpf.tools import queries as _queries

# Store the current GEONIS language globally, once it has been determined
_gn_lang = None


class _Definition(object):
    """ Base class for all definition mappings. """
    __slots__ = '_def'

    def __init__(self, definitions):
        _vld.pass_if(isinstance(definitions, DefinitionTable), ValueError,
                     "'definitions' argument must be a DefinitionTable instance")
        self._def = definitions


class _EleTableNames(_Definition):
    """
    Provides access to GEONIS ELE table names for the given definition table (electric solution).

    **Params:**

    -   **definition** (:class:`DefinitionTable`):

        A DefinitionTable instance. The table must fit the electric solution.
    """

    strand = property(lambda self: self._def.get('tablename_branch', 'ele_strang'))
    cable = property(lambda self: self._def.get('tablename_cable', 'ele_kabel'))
    clamp = property(lambda self: self._def.get('tablename_clamp', 'ele_ds_klemme'))
    construction_line = property(lambda self: self._def.get('tablename_construction_line', 'ele_bauobjekt_lin'))
    cs_base = property(lambda self: self._def.get('tablename_cs_base', 'ele_qs_basis'))
    cs_cable = property(lambda self: self._def.get('tablename_cs_cable', 'ele_qs_kabel'))
    cs_area = property(lambda self: self._def.get('tablename_cs_frame', 'ele_qs_fla'))
    cs_pipe = property(lambda self: self._def.get('tablename_cs_pipe', 'ele_qs_rohr'))
    cs_pipe_pipe = property(lambda self: self._def.get('tablename_cs_pipepipe', 'ele_qs_rohr_rohr'))
    cs_cable_protect_pos = property(lambda self: self._def.get('tablename_cs_posnum_label', 'elet_qs_kabelschutzpos'))
    ds_connector = property(lambda self: self._def.get('tablename_ds_connector', 'ele_ds_verbinder'))
    ds_cable_connector = property(lambda self: self._def.get('tablename_ds_cableconnector', 'ele_ds_kabelverbindung'))
    ds_transition = property(lambda self: self._def.get('tablename_ds_inout', 'ele_ds_uebergang'))
    ds_station = property(lambda self: self._def.get('tablename_ds_station', 'ele_ds_station'))
    ds_transformer = property(lambda self: self._def.get('tablename_ds_transformer', 'ele_ds_transformer'))
    house = property(lambda self: self._def.get('tablename_house_conn', 'ele_hausanschluss'))
    lighting = property(lambda self: self._def.get('tablename_luminary', 'ele_leuchte'))
    pipe = property(lambda self: self._def.get('tablename_pipe', 'ele_rohr'))
    rel_cable_route = property(lambda self: self._def.get('tablename_route_cable', 'eler_trasse_kabel'))
    rel_pipe_cable = property(lambda self: self._def.get('tablename_pipe_cable', 'eler_rohr_kabel'))
    rel_pipe_pipe = property(lambda self: self._def.get('tablename_pipe_pipe', 'eler_rohr_rohr'))
    rel_route_rohr = property(lambda self: self._def.get('tablename_route_pipe', 'eler_route_pipe'))
    route = property(lambda self: self._def.get('tablename_route', 'ele_trasse'))
    sec_cable_voltage = property(lambda self: self._def.get('tablename_sec_cable_dense', 'eles_spannung'))
    sec_cable_protect = property(lambda self: self._def.get('tablename_sec_cable_protect', 'eles_kabelschutz_rohr'))
    sec_cs_cable = property(lambda self: self._def.get('tablename_sec_cable_cs', 'eles_querschnitt_kabel'))
    sec_cs_route = property(lambda self: self._def.get('tablename_typ_querschnitt', 'eles_querschnitt_trasse'))
    sec_cs_scaling = property(lambda self: self._def.get('tablename_querschnitt_skalierung',
                                                         'eles_querschnitt_skalierung'))
    sec_net_color = property(lambda self: self._def.get('tablename_sec_netcolor', 'eles_netzfarbe'))
    sec_type_dd = property(lambda self: self._def.get('tablename_typ_ds', 'eles_typ_ds'))
    sec_type_route = property(lambda self: self._def.get('tablename_typ_trasse', 'eles_typ_trasse'))
    sleeve = property(lambda self: self._def.get('tablename_sleeve_socket', 'ele_muffe'))
    small_connection = property(lambda self: self._def.get('tablename_small_conn', 'ele_kleinanschluss'))
    t_cs_cable = property(lambda self: self._def.get('tablename_t_cs_cable', 'elet_qs_kabel'))
    t_cs_rohr = property(lambda self: self._def.get('tablename_t_cs_pipe', 'elet_qs_rohr'))
    t_cs_rohr_rohr = property(lambda self: self._def.get('tablename_t_cs_pipe_pipe', 'elet_qs_rohr_rohr'))


class _EleFieldNames(_Definition):
    """
    Provides access to GEONIS ELE field names for the given definition table (electric solution).

    **Params:**

    -   **definition** (:class:`DefinitionTable`):

        A DefinitionTable instance. The table must fit the electric solution.
    """

    cable_protect = property(lambda self: self._def.get('fieldname_cable_protect', 'kabelschutz'))
    cable_ref = property(lambda self: self._def.get('fieldname_cable_ref', 'kabel_ref'))
    clamp_number = property(lambda self: self._def.get('fieldname_clamp_number', 'nummer'))
    code_ref = property(lambda self: self._def.get('fieldname_code_ref', 'code'))
    cs_angle = property(lambda self: self._def.get('fieldname_cs_angle', 'symbolori'))
    cs_mapscale = property(lambda self: self._def.get('fieldname_cs_mapscale', 'mapscale'))
    cs_ref = property(lambda self: self._def.get('fieldname_cs_ref', 'qs_ref'))
    cs_released = property(lambda self: self._def.get('fieldname_cs_released', 'released'))
    cs_type = property(lambda self: self._def.get('fieldname_cs_typ', 'querschnitt'))
    cs_visible = property(lambda self: self._def.get('fieldname_cs_visible', 'visible'))
    cs_width = property(lambda self: self._def.get('fieldname_cs_width', 'breite'))
    dd_ref = property(lambda self: self._def.get('fieldname_ds_ref', 'ds_ref'))
    ddhv_ref = property(lambda self: self._def.get('fieldname_dshs_ref', 'dshs_ref'))
    ddlv_ref = property(lambda self: self._def.get('fieldname_dsns_ref', 'dsns_ref'))
    ddmv_ref = property(lambda self: self._def.get('fieldname_dsms_ref', 'dsms_ref'))
    ddpl_ref = property(lambda self: self._def.get('fieldname_dsob_ref', 'dsob_ref'))
    info_text = property(lambda self: self._def.get('fieldname_elementinfo', 'infotext'))
    feature_link = property(lambda self: self._def.get('fieldname_featurelink', 'featurelink'))
    index = property(lambda self: self._def.get('fieldname_idx', 'idx'))
    ipipe_ref = property(lambda self: self._def.get('fieldname_ipipe_ref', 'inner_rohr_ref'))
    length = property(lambda self: self._def.get('fieldname_length', 'laenge'))
    opipe_ref = property(lambda self: self._def.get('fieldname_opipe_ref', 'ueber_rohr_ref'))
    pipe_ref = property(lambda self: self._def.get('fieldname_pipe_ref', 'rohr_ref'))
    position = property(lambda self: self._def.get('fieldname_posnum', 'posnum'))
    route_index = property(lambda self: self._def.get('fieldname_trench_idx', 'trasse_idx'))
    route_pos = property(lambda self: self._def.get('fieldname_trench_pos', 'trasse_pos'))
    route_ref = property(lambda self: self._def.get('fieldname_route_ref', 'trasse_ref'))
    route_reverse = property(lambda self: self._def.get('fieldname_trench_reverse', 'reverse'))
    route_type = property(lambda self: self._def.get('fieldname_trasse_typ', 'typ'))
    station_ref = property(lambda self: self._def.get('fieldname_station_ref', 'station_ref'))
    strand_ref = property(lambda self: self._def.get('fieldname_strang_ref', 'strang_ref'))
    text_ori = property(lambda self: self._def.get('fieldname_text_angle', 'textori'))
    transformer_number = property(lambda self: self._def.get('fieldname_ds_trafo_name_number', 'name_nummer'))
    transformer_power = property(lambda self: self._def.get('fieldname_trafo_power', 'leistung'))
    transformer_ref = property(lambda self: self._def.get('fieldname_trafo_ref', 'trafo_ref'))
    voltage = property(lambda self: self._def.get('fieldname_dense', 'spannung'))

    # The following property seems a bit odd, but this is actually how its determined in the GEONIS core code...
    name_number = property(lambda self:
                           'name_nummer' if _EleTableNames(self._def).sec_cable_voltage == 'eles_spannung'
                           else 'name_number')

    @property
    def description(self):
        """ Determines the current GEONIS language and returns the matching description field name for it. """
        global _gn_lang

        # Only read the language once and store it on the global module level
        _gn_lang = _gn_lang or _i18n.get_language()

        return {
            _i18n.GN_LANG_CUSTOM: _const.GNFIELD_DESC_CUSTOM,
            _i18n.GN_LANG_DE:     _const.GNFIELD_DESC_DE,
            _i18n.GN_LANG_EN:     _const.GNFIELD_DESC_EN,
            _i18n.GN_LANG_FR:     _const.GNFIELD_DESC_FR,
            _i18n.GN_LANG_IT:     _const.GNFIELD_DESC_IT
        }.get(_gn_lang, _const.GNFIELD_DESC_DE)


class DefinitionTable(_lookups.ValueLookup):
    """
    Class that exposes the definitions (named objects) within the GEONIS data model.

    **Params:**

    -   **workspace** (gpf.paths.Workspace):

        The Workspace instance for the GEONIS database.

    -   **solution** (str, unicode):

        The name of the solution (e.g. ELE, GAS etc.) for which to read the definitions.
    """

    def __init__(self, workspace, solution):

        # Check if workspace is a Workspace instance
        _vld.pass_if(isinstance(workspace, _paths.Workspace), ValueError,
                     '{!r} requires a {} object'.format(DefinitionTable.__name__, _paths.Workspace.__name__))

        # Construct definition table path for the given workspace and solution
        table_path = str(workspace.make_path(_const.GNTABLE_SOLUTION_DEF.format(solution)))

        try:
            # Try and get a lookup for the solution
            super(DefinitionTable, self).__init__(table_path, _const.GNFIELD_NAME, _const.GNFIELD_VALUE)
        except RuntimeError:
            raise RuntimeError("Failed to read GEONIS definition table for the '{}' solution".format(solution.upper()))

        if not self:
            # The table is empty: this should never happen under normal circumstances
            raise ValueError('There are no definitions for the {} solution'.format(solution.upper()))

        self._solution = solution.lower()

    @property
    def solution(self):
        """ Returns the (lowercase) solution name to which this definitions table applies. """
        return self._solution


class EleDefinitions(DefinitionTable):

    def __init__(self, workspace):
        super(EleDefinitions, self).__init__(workspace, _const.GNMEDIA_ELECTRIC)

    @property
    def tables(self):
        """ Provides access to GEONIS table names for the ELE solution. """
        return _EleTableNames(self)

    @property
    def fields(self):
        """ Provides access to GEONIS field names for the ELE solution. """
        return _EleFieldNames(self)


class Relation(tuple):
    """
    Simple dataholder (similar to a ``namedtuple``) for a GEONIS table relation.
    These type of objects are stored as values in a :class:`RelationTable` lookup dictionary.
    The source table name for the relation is taken from the key in this dictionary.

    The initialization argument names are equal to the listed property names below.
    """
    __slots__ = ()

    def __new__(cls, target_table=None, relate_table=None, source_field=None, target_field=None,
                relate_source=None, relate_target=None, relate_type=None):
        args = cls._fix_args(target_table, relate_table, source_field, target_field,
                             relate_source, relate_target, relate_type)
        return tuple.__new__(Relation, args)

    @classmethod
    def _fix_args(cls, *args):
        for i in xrange(cls.__new__.func_code.co_argcount - 1):
            try:
                yield args[i]
            except IndexError:
                yield None

    def __nonzero__(self):
        # If all values in the tuple are None, return False.
        return any(self)

    #: The name of the target/destination table that stores the foreign key field.
    target_table = property(lambda self: self[0])

    #: The name of the relation table (if cardinality is n:m).
    relate_table = property(lambda self: self[1])

    #: The name of the primary key field in the source/origin table.
    source_field = property(lambda self: self[2])

    #: The name of the foreign key field in the target/destination table.
    target_field = property(lambda self: self[3])

    #: The name of the source reference field in the relationship table (if cardinality is n:m).
    relate_source = property(lambda self: self[4])

    #: The name of the target reference field in the relationship table (if cardinality is n:m).
    relate_target = property(lambda self: self[5])

    #: The relationship type or cardinality (e.g. "1:n", "1:1", "n:m", "1:0").
    relate_type = property(lambda self: self[6])


class RelationWarning(UserWarning):
    """ Warning that is shown when a bad relation has been detected in the GEONIS relationship table. """
    pass


class RelationTable(_lookups.Lookup):
    """
    Class that returns the relationship table for the GEONIS data model as a lookup dictionary.

    Each key in the dictionary either represents the name of the source table (default) or the target table,
    depending on the value of the *reverse* argument.

    For each key, a :class:`Relation` is returned with the:

    -   target table (value of source table if *reverse* is ``True``)
    -   relationship table (``None`` if not set)
    -   source key field (target reference field if *reverse* is ``True``)
    -   target reference field (source key field if *reverse* is ``True``)
    -   relationship source reference field (``None`` if not set, target reference field if *reverse* is ``True``)
    -   relationship target reference field (``None`` if not set, source reference field if *reverse* is ``True``)
    -   relation type name

    Note that the relationship table values will only be set if the cardinality of the relationship is *n:m*.

    **Params:**

    -   **workspace** (gpf.paths.Workspace):

        The Workspace instance for the GEONIS database.

    -   **relation_type** (str, unicode):

        An optional name of the relationship type (on which to filter).
        Note that the :py:mod:`gntools.common.const` module contains all the
        relationship type names (constants starting with GNRELTYPE_*).

    -   **reverse** (bool):

        If set to ``True``, the relationship is mapped from target to source. The default is ``False``.

    .. seealso::    :class:`Relation`
    """

    def __init__(self, workspace, relation_type, reverse=False):

        rel_types = (_const.GNRELTYPE_AGGREGRATE, _const.GNRELTYPE_COMPOSITE, _const.GNRELTYPE_DATALINK,
                     _const.GNRELTYPE_ENTITY, _const.GNRELTYPE_LABEL, _const.GNRELTYPE_PLAN,
                     _const.GNRELTYPE_RELATE, _const.GNRELTYPE_SHAPEGROUP)

        # Check if workspace is a Workspace instance and that a valid relation_type has been set
        _vld.pass_if(isinstance(workspace, _paths.Workspace), ValueError,
                     '{!r} requires a {} object'.format(DefinitionTable.__name__, _paths.Workspace.__name__))
        _vld.pass_if(relation_type in rel_types, ValueError,
                     'relation_type must be one of {}'.format(_tu.format_iterable(rel_types, _const.TEXT_OR)))

        # Construct relation definition table path and where clause
        table_path = str(workspace.make_path(_const.GNTABLE_RELATION_DEF))
        type_filter = _queries.Where(_const.GNFIELD_REL_TYPE).Equals(relation_type)

        # Define required field default names
        src_table = _const.GNFIELD_REL_TABLE_SRC
        dst_table = _const.GNFIELD_REL_TABLE_DST
        src_field = _const.GNFIELD_REL_KEYFIELD_SRC
        dst_field = _const.GNFIELD_REL_KEYFIELD_DST
        src_rel = _const.GNFIELD_REL_RELFIELD_SRC
        dst_rel = _const.GNFIELD_REL_RELFIELD_DST

        # Switch source and destination fields if 'reverse' is True
        if reverse:
            src_table = _const.GNFIELD_REL_TABLE_DST
            dst_table = _const.GNFIELD_REL_TABLE_SRC
            src_field = _const.GNFIELD_REL_KEYFIELD_DST
            dst_field = _const.GNFIELD_REL_KEYFIELD_SRC
            src_rel = _const.GNFIELD_REL_RELFIELD_DST
            dst_rel = _const.GNFIELD_REL_RELFIELD_SRC

        # Set fields to collect
        fields = (dst_table, _const.GNFIELD_REL_TABLE_REL, src_field,
                  dst_field, src_rel, dst_rel, _const.GNFIELD_REL_TYPE)

        try:
            # Try and build a relationship lookup
            super(RelationTable, self).__init__(table_path, src_table, fields, type_filter)
        except RuntimeError as e:
            raise RuntimeError("Failed to read GEONIS relation table '{}': {}".format(table_path, e))

    def _process_row(self, row, **kwargs):
        """ Stores each row in the relationship definition table as ``Relation`` objects. """
        formatted = [(v.upper().strip() if isinstance(v, basestring) else v) for v in row]
        key, values = formatted[0], Relation(*formatted[1:])
        if not key:
            return
        if key in self:
            _warn("Source table '{}' participates in multiple {} relationships".format(key.upper(), values.relate_type),
                  RelationWarning)
            return
        self[key] = values
