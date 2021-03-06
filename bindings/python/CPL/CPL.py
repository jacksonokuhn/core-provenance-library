#!/usr/bin/env python

#
# setup.py
# Core Provenance Library
#
# Copyright 2012
#      The President and Fellows of Harvard College.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE UNIVERSITY OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# Contributor(s): Margo Seltzer, Peter Macko
#

'''
Class and functions supporting the Python bindings of the 'Core Provenance
Library <http://http://code.google.com/p/core-provenance-library/>'_.

This module contains:

*	The cpl class.
*	The cpl_ancestor class.
*	The cpl_session class.
*	The cpl_session_info class.
*	The cpl_object class.
*	The cpl_object_info class.
*	The cpl_object_version class.
*	The cpl_object_version_info class.
*	Helper functions to print and construct cpl objects
'''

import sys
import CPLDirect


#
# Constants
#

NONE = CPLDirect.CPL_NONE
VERSION_NONE = CPLDirect.CPL_VERSION_NONE
DEPENDENCY_CATEGORY_DATA = CPLDirect.CPL_DEPENDENCY_CATEGORY_DATA
DEPENDENCY_CATEGORY_CONTROL = CPLDirect.CPL_DEPENDENCY_CATEGORY_CONTROL
DEPENDENCY_CATEGORY_VERSION = CPLDirect.CPL_DEPENDENCY_CATEGORY_VERSION
DEPENDENCY_NONE = CPLDirect.CPL_DEPENDENCY_NONE
DATA_INPUT = CPLDirect.CPL_DATA_INPUT
DATA_GENERIC = CPLDirect.CPL_DATA_GENERIC
DATA_IPC = CPLDirect.CPL_DATA_IPC
DATA_TRANSLATION = CPLDirect.CPL_DATA_TRANSLATION
DATA_COPY = CPLDirect.CPL_DATA_COPY
CONTROL_OP = CPLDirect.CPL_CONTROL_OP
CONTROL_GENERIC = CPLDirect.CPL_CONTROL_GENERIC
CONTROL_START = CPLDirect.CPL_CONTROL_START
VERSION_PREV = CPLDirect.CPL_VERSION_PREV
VERSION_GENERIC = CPLDirect.CPL_VERSION_GENERIC
S_OK = CPLDirect.CPL_S_OK
OK = CPLDirect.CPL_OK
S_DUPLICATE_IGNORED = CPLDirect.CPL_S_DUPLICATE_IGNORED
S_NO_DATA = CPLDirect.CPL_S_NO_DATA
S_OBJECT_CREATED = CPLDirect.CPL_S_OBJECT_CREATED
E_INVALID_ARGUMENT = CPLDirect.CPL_E_INVALID_ARGUMENT
E_INSUFFICIENT_RESOURCES = CPLDirect.CPL_E_INSUFFICIENT_RESOURCES
E_DB_CONNECTION_ERROR = CPLDirect.CPL_E_DB_CONNECTION_ERROR
E_NOT_IMPLEMENTED = CPLDirect.CPL_E_NOT_IMPLEMENTED
E_ALREADY_INITIALIZED = CPLDirect.CPL_E_ALREADY_INITIALIZED
E_NOT_INITIALIZED = CPLDirect.CPL_E_NOT_INITIALIZED
E_PREPARE_STATEMENT_ERROR = CPLDirect.CPL_E_PREPARE_STATEMENT_ERROR
E_STATEMENT_ERROR = CPLDirect.CPL_E_STATEMENT_ERROR
E_INTERNAL_ERROR = CPLDirect.CPL_E_INTERNAL_ERROR
E_BACKEND_INTERNAL_ERROR = CPLDirect.CPL_E_BACKEND_INTERNAL_ERROR
E_NOT_FOUND = CPLDirect.CPL_E_NOT_FOUND
E_ALREADY_EXISTS = CPLDirect.CPL_E_ALREADY_EXISTS
E_PLATFORM_ERROR = CPLDirect.CPL_E_PLATFORM_ERROR
E_INVALID_VERSION = CPLDirect.CPL_E_INVALID_VERSION
E_DB_NULL = CPLDirect.CPL_E_DB_NULL
E_DB_KEY_NOT_FOUND = CPLDirect.CPL_E_DB_KEY_NOT_FOUND
E_DB_INVALID_TYPE = CPLDirect.CPL_E_DB_INVALID_TYPE
O_FILESYSTEM = CPLDirect.CPL_O_FILESYSTEM
O_INTERNET = CPLDirect.CPL_O_INTERNET
T_ARTIFACT = CPLDirect.CPL_T_ARTIFACT
T_FILE = CPLDirect.CPL_T_FILE
T_PROCESS = CPLDirect.CPL_T_PROCESS
T_URL = CPLDirect.CPL_T_URL
L_NO_FAIL = CPLDirect.CPL_L_NO_FAIL
I_NO_CREATION_SESSION = CPLDirect.CPL_I_NO_CREATION_SESSION
I_NO_VERSION = CPLDirect.CPL_I_NO_VERSION
I_FAST = CPLDirect.CPL_I_FAST
D_ANCESTORS = CPLDirect.CPL_D_ANCESTORS
D_DESCENDANTS = CPLDirect.CPL_D_DESCENDANTS
A_NO_PREV_NEXT_VERSION = CPLDirect.CPL_A_NO_PREV_NEXT_VERSION
A_NO_DATA_DEPENDENCIES = CPLDirect.CPL_A_NO_DATA_DEPENDENCIES
A_NO_CONTROL_DEPENDENCIES = CPLDirect.CPL_A_NO_CONTROL_DEPENDENCIES
F_LOOKUP_ONLY = 0
F_ALWAYS_CREATE = CPLDirect.CPL_F_ALWAYS_CREATE
F_CREATE_IF_DOES_NOT_EXIST = CPLDirect.CPL_F_CREATE_IF_DOES_NOT_EXIST



#
# Private constants
#

__data_dict = ['data input', 'data ipc', 'data translation', 'data copy']
__control_dict = ['control op', 'control start']


#
# Global variables
#

_cpl_connection = None



#
# Private utility functions
#

def __getSignedNumber(number, bitLength):
	'''
	Print out a long value as a signed bitLength-sized integer.
	Thanks to:
	http://stackoverflow.com/questions/1375897/how-to-get-the-signed-integer-value-of-a-long-in-python
	for this function.
	'''
	mask = (2 ** bitLength) - 1
	if number & (1 << (bitLength - 1)):
		return number | ~mask
	else:
		return number & mask



#
# CPLDirect enhancements
#

def __cpl_id_t__eq__(self, other):
	'''
	Compare this and another ID, and return true if they are equal
	'''
	return self.lo == other.lo and self.hi == other.hi


def __cpl_id_t__ne__(self, other):
	'''
	Compare this and another ID, and return true if they are not equal
	'''
	return self.lo != other.lo  or self.hi != other.hi


def __cpl_id_t__str__(self):
	'''
	Create and return a string representation of this object
	'''
	return "%x:%x" % (self.hi, self.lo)


CPLDirect.cpl_id_t.__eq__ = __cpl_id_t__eq__
CPLDirect.cpl_id_t.__ne__ = __cpl_id_t__ne__
CPLDirect.cpl_id_t.__str__ = __cpl_id_t__str__



#
# Public utility functions
#

def current_connection():
	'''
	Return the current CPL connection object, or None if not connected
	'''
	global _cpl_connection
	return _cpl_connection


def dependency_type_to_str(val):
	'''
	Given a dependency (edge) type, convert it to a string

	Method calls::
		strval = dependency_type_to_str(val)
	'''
	which = val >> 8
	if which == DEPENDENCY_CATEGORY_DATA:
		if (val & 7) < len(__data_dict):
			return __data_dict[val & 7]
		else:
			return 'data unknown'
	elif which == DEPENDENCY_CATEGORY_CONTROL:
		if (val & 7) < len(__control_dict):
			return __control_dict[val & 7]
		else:
			return 'control unknown'
	elif which == DEPENDENCY_CATEGORY_VERSION:
		return 'version'
	else:
		return 'unknown'


def copy_id(idp):
	'''
	Construct a cpl identifier type consisting of the hi and lo values.

	Method calls::
		id = copy_id(idp)
	'''
	i = CPLDirect.cpl_id_t()
	i.hi = idp.hi
	i.lo = idp.lo
	return i


def p_id(id, with_newline = False):
	'''
	Print hi and lo fields of a CPL id, optionally with newline after it.

	Method calls::
		p_id(id, with_newline = False)
	'''
	sys.stdout.write('id: ' + str(id))
	if with_newline:
		sys.stdout.write('\n')


def p_object(obj, with_session = False):
	'''
	Print information about an object

	Method calls:
		p_object(obj, with_session = False)
	'''
	i = obj.info()
	p_id(i.object.id)
	print(' version: ' + str(i.version))
	sys.stdout.write('container_id: ')
	if i.container is not None:
		p_id(i.container.object.id)
		print(' container version: ' + str(i.container.version))
	else:
		sys.stdout.write('none')
		print(' container version: none')
	print('originator: ' + i.originator + ' name:' + i.name +
	    ' type: ' + i.type)
	if with_session:
		print('creation_time: ' + str(i.creation_time))
		p_session(i.creation_session)


def p_object_version(obj_ver, with_session = False):
	'''
	Print information about a version of an object

	Method calls:
		p_object_version(obj_ver, with_session = False)
	'''
	print(str(obj_ver))
	i = obj_ver.info()
	if with_session:
		print('creation_time: ' + str(i.creation_time))
		p_session(i.session)


def p_session(session):
	'''
	Print information about a session

	Method calls:
		p_session(session)
	'''
	si = session.info()
	sys.stdout.write('session ')
	p_id(si.session.id, with_newline = True)
	print(' mac_address: ' + si.mac_address + ' pid: ' + str(si.pid))
	print('\t(' + str(si.start_time) + ')' + ' user: ' +
	    si.user + ' cmdline: ' + si.cmdline + ' program: ' + si.program)



#
# Information about a specific version of a provenance object
#

class cpl_object_version_info:
	'''
	Information about a specific version of a provenance object
	'''

	def __init__(self, object_version, session, creation_time):
		'''
		Create an instance of this object
		'''

		self.object_version = object_version
		self.session = session
		self.creation_time = creation_time



#
# Object & version
#

class cpl_object_version:
	'''
	Stores a reference to a provenance object and a version number
	'''


	def __init__(self, object, version):
		'''
		Create an instance of this object
		''',
		self.object = object
		self.version = version


	def __eq__(self, other):
		'''
		Compare this and the other object, and return true if they are equal
		'''
		return self.object.id==other.object.id and self.version==other.version


	def __ne__(self, other):
		'''
		Compare this and the other object, and return true if they are not equal
		'''
		return self.object.id!=other.object.id or self.version!=other.version


	def __str__(self):
		'''
		Create and return a human-readable string representation of this object
		'''
		return str(self.object) + '-' + str(self.version)


	def info(self):
		'''
		Return the corresponding cpl_object_version_info for this specific
		version of the object.
		'''

		infopp = CPLDirect.new_cpl_version_info_tpp()

		ret = CPLDirect.cpl_get_version_info(self.object.id, self.version,
		    CPLDirect.cpl_convert_pp_cpl_version_info_t(infopp))
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_cpl_version_info_tpp(infopp)
			raise Exception('Unable to get object version info: ' +
					CPLDirect.cpl_error_string(ret))

		op = CPLDirect.cpl_dereference_pp_cpl_version_info_t(infopp)
		info = CPLDirect.cpl_version_info_tp_value(op)

		_info = cpl_object_version_info(self, cpl_session(info.session),
				info.creation_time)

		CPLDirect.cpl_free_version_info(op)
		CPLDirect.delete_cpl_version_info_tpp(infopp)

		return _info


	def control_flow_to(self, dest, type=CONTROL_OP):
		'''
		Add a control flow edge of type from self to dest.
		'''
		return self.object.control_flow_to(dest, type, self.version)


	def data_flow_to(self, dest, type=DATA_INPUT):
		'''
		Add a data flow edge of type from self to dest.
		'''
		return self.object.data_flow_to(dest, type, self.version)


#
# Provenance ancestry entry
#

class cpl_ancestor:
	'''
	Stores the same data as a cpl_ancestry_entry_t, but in a Python
	class that we manage.
	'''


	def __init__(self, aid, aversion, did, dversion, type, direction):
		'''
		Create an instance of cpl_ancestor
		'''
		self.ancestor = cpl_object_version(cpl_object(aid), aversion)
		self.descendant = cpl_object_version(cpl_object(did), dversion)
		self.type = type

		if direction == D_ANCESTORS:
			self.base  = self.descendant
			self.other = self.ancestor
		else:
			self.base  = self.ancestor
			self.other = self.descendant


	def __str__(self):
		'''
		Create a printable string representation of this object
		'''
		
		arrow = ' -- '
		if self.other == self.ancestor:
			arrow = ' --> '
		else:
			arrow = ' <-- '
		return (str(self.base) + arrow + str(self.other) +
			' type:' + dependency_type_to_str(self.type))



#
# CPL Connection
#

class cpl_connection:
	'''
	Core provenance library connection -- maintains state for the current
	session and the current database backend.
	'''


	def __init__(self, cstring="DSN=CPL;"):
		'''
		Constructor for CPL connection.

		** Parameters **
			** cstring **
			Connection string for database backend

		** Note **
		Currently the python bindings support only ODBC connection.
		RDF connector coming soon.
		'''
		global _cpl_connection

		self.connection_string = cstring
		self.closed = False

		def get_current_session():
			idp = CPLDirect.new_cpl_id_tp()
			ret = CPLDirect.cpl_get_current_session(idp)

			if not CPLDirect.cpl_is_ok(ret):
				CPLDirect.delete_cpl_id_tp(idp)
				raise Exception("Could not get current session" +
				       CPLDirect.cpl_error_string(ret))

			s = CPLDirect.cpl_id_tp_value(idp)
			i = copy_id(s)
			CPLDirect.delete_cpl_id_tp(idp)
			return i

		backend = CPLDirect.new_cpl_db_backend_tpp()
		ret = CPLDirect.cpl_create_odbc_backend(cstring,
		    CPLDirect.CPL_ODBC_GENERIC, backend)
		if not CPLDirect.cpl_is_ok(ret):
			raise Exception("Could not create ODBC connection" +
			       CPLDirect.cpl_error_string(ret))
		self.db = CPLDirect.cpl_dereference_pp_cpl_db_backend_t(backend)
		ret = CPLDirect.cpl_attach(self.db)
		CPLDirect.delete_cpl_db_backend_tpp(backend)
		if not CPLDirect.cpl_is_ok(ret):
			raise Exception("Could not open ODBC connection" +
			       CPLDirect.cpl_error_string(ret))
		self.session = cpl_session(get_current_session())

		_cpl_connection = self


	def __del__(self):
		'''
		Destructor - automatically closes the connection.
		'''
		if self == _cpl_connection and not self.closed:
			self.close()


	def __create_or_lookup_cpl_object(self, originator,
		     name, type, create=None, container=None):
		'''
		Create or lookup a CPL object

		** Parameters **
			originator 
			name: originator-local name
			type: originator-local type
			create:
				None: lookup or create
				True: create only
				False: lookup only
			container:
				Id of container into which to place this object.
				Only applies to create
		'''
		if container is None:
			container_id = NONE
		else:
			container_id = container.id

		idp = CPLDirect.new_cpl_id_tp()
		if create == None:
			ret = CPLDirect.cpl_lookup_or_create_object(originator, name,
							  type, container_id, idp)
			if ret == S_OBJECT_CREATED:
				ret = S_OK
		elif create:
			ret = CPLDirect.cpl_create_object(originator,
						name, type, container_id, idp)
		else:
			ret = CPLDirect.cpl_lookup_object(originator, name, type, idp)

		if ret == E_NOT_FOUND:
			CPLDirect.delete_cpl_id_tp(idp)
			raise LookupError('Not found')
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_cpl_id_tp(idp)
			raise Exception('Could not find or create' +
			    ' provenance object: ' + CPLDirect.cpl_error_string(ret))
			
		r = cpl_object(idp)

		CPLDirect.delete_cpl_id_tp(idp)
		return r


	def get_all_objects(self, fast=False):
		'''
		Return all objects in the provenance database. If fast = True, then
		fetch only incomplete information about each object, so that it is
		faster.
		'''

		if fast:
			flags = CPLDirect.CPL_I_FAST
		else:
			flags = 0

		vp = CPLDirect.new_std_vector_cplxx_object_info_tp()
		ret = CPLDirect.cpl_get_all_objects(flags,
			CPLDirect.cpl_cb_collect_object_info_vector, vp)

		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_std_vector_cplxx_object_info_tp(vp)
			raise Exception('Unable to get all objects: ' +
					CPLDirect.cpl_error_string(ret))

		v = CPLDirect.cpl_dereference_p_std_vector_cplxx_object_info_t(vp)
		l = []
		if v != S_NO_DATA :
			for e in v:
				if e.container_id == NONE or e.container_version < 0:
					container = None
				else:
					container = cpl_object_version(cpl_object(e.container_id),
							e.container_version)
				if e.creation_session == NONE:
					creation_session = None
				else:
					creation_session = cpl_session(e.creation_session)
				l.append(cpl_object_info(cpl_object(e.id), e.version,
					creation_session, e.creation_time, e.originator, e.name,
					e.type, container))

		CPLDirect.delete_std_vector_cplxx_object_info_tp(vp)
		return l
			

	def get_object(self, originator, name, type, container=None):
		'''
		Get the object, with the designated originator (string),
		name (string), and type (string), creating it if necessary.

		If you want an object in a specific container, set the container
		parameter to the ID of the object in which you want this object
		created.
		'''
		return self.__create_or_lookup_cpl_object(originator, name, type,
				create=None, container=container)


	def create_object(self, originator, name, type, container=None):
		'''
		Create object, returns None if object already exists.
		'''
		return self.__create_or_lookup_cpl_object(originator, name, type,
				create=True, container=container)


	def lookup_object(self, originator, name, type):
		'''
		Look up object; raise LookupError if the object does not exist.
		'''
		o = self.__create_or_lookup_cpl_object(originator, name, type,
				create=False)
		return o


	def try_lookup_object(self, originator, name, type):
		'''
		Look up object; returns None if the object does not exist.
		'''
		try:
			o = self.__create_or_lookup_cpl_object(originator, name, type,
					create=False)
		except LookupError:
			o = None
		return o


	def lookup_by_property(self, key, value):
		'''
		Return all objects that have the key/value property specified; raise
		LookupError if no such object is found.
		'''
		vp = CPLDirect.new_std_vector_cpl_id_version_tp()
		ret = CPLDirect.cpl_lookup_by_property(key, value,
			CPLDirect.cpl_cb_collect_property_lookup_vector, vp)

		if ret == E_NOT_FOUND:
			CPLDirect.delete_std_vector_cpl_id_version_tp(vp)
			raise LookupError('Not found')
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_std_vector_cpl_id_version_tp(vp)
			raise Exception('Unable to lookup by property ' +
					CPLDirect.cpl_error_string(ret))

		v = CPLDirect.cpl_dereference_p_std_vector_cpl_id_version_t(vp)
		l = []
		for e in v:
			l.append(cpl_object_version(cpl_object(e.id), e.version))

		CPLDirect.delete_std_vector_cpl_id_version_tp(vp)
		return l


	def try_lookup_by_property(self, key, value):
		'''
		Return all objects that have the key/value property specified, but do
		not fail if no such object is found -- return an empty list instead.
		'''
		try:
			o = self.lookup_by_property(key, value)
		except LookupError:
			o = []
		return o


	def lookup_all(self, originator, name, type):
		'''
		Return all objects that have the specified originator, name,
		and type (they might differ by container).
		'''
		vp = CPLDirect.new_std_vector_cpl_id_timestamp_tp()
		ret = CPLDirect.cpl_lookup_object_ext(originator, name, type,
			L_NO_FAIL, CPLDirect.cpl_cb_collect_id_timestamp_vector, vp)

		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_std_vector_cpl_id_timestamp_tp(vp)
			raise Exception('Unable to lookup all objects: ' +
					CPLDirect.cpl_error_string(ret))

		v = CPLDirect.cpl_dereference_p_std_vector_cpl_id_timestamp_t(vp)
		l = []
		if v != S_NO_DATA :
			for e in v:
				l.append(cpl_object(e.id))

		CPLDirect.delete_std_vector_cpl_id_timestamp_tp(vp)
		return l


	def get_object_for_file(self, file_name, mode=F_CREATE_IF_DOES_NOT_EXIST):
		'''
		Get or create (depending on the value of mode) a provenance object
		that corresponds to the given file on the file system. The file must
		already exist.

		Please note that the CPL internally refers to the files using their
		full path, so if you move the file by a utility that is not CPL-aware,
		a subsequent call to this function with the same file (after it has
		been moved or renamed) will not find the return back the same
		provenance object. Furthermore, beware that if you use hard links,
		you will get different provenance objects for different names/paths
		of the file.
		
		The mode can be one of the following values:
			* F_LOOKUP_ONLY: Perform only the lookup -- do not create the
			  corresponding provenance object if it does not already exists.
			* F_CREATE_IF_DOES_NOT_EXIST: Create the corresponding provenance
			  object if it does not already exist (this is the default).
			* F_ALWAYS_CREATE: Always create a new corresponding provenance
			  object, even if it already exists. Use this if you completely
			  overwrite the file.
		'''

		idp = CPLDirect.new_cpl_id_tp()
		vp  = CPLDirect.new_cpl_version_tp()

		ret = CPLDirect.cpl_lookup_file(file_name, mode, idp, vp)
		if not CPLDirect.cpl_is_ok(ret):
			raise Exception('Could not find or create provenance object' +
			    ' for a file: ' + CPLDirect.cpl_error_string(ret))
			
		r = cpl_object(idp)

		CPLDirect.delete_cpl_id_tp(idp)
		CPLDirect.delete_cpl_version_tp(vp)
		return r


	def create_object_for_file(self, file_name):
		'''
		Create a provenance object that corresponds to the specified file.
		This function is equivalent to calling get_object_for_file() with
		mode = F_ALWAYS_CREATE.
		'''
		return self.get_object_for_file(file_name, F_ALWAYS_CREATE)


	def close(self):
		'''
		Close database connection and session
		'''
		global _cpl_connection
		
		if self != _cpl_connection or self.closed:
			return

		ret = CPLDirect.cpl_detach()
		if not CPLDirect.cpl_is_ok(ret):
			raise Exception('Could not detach ' +
					CPLDirect.cpl_error_string(ret))

		_cpl_connection = None
		self.closed = True



#
# Information about a provenance session
#

class cpl_session_info:
	'''
	Information about a provenance session
	'''

	def __init__(self, session, mac_address, user, pid, program, cmdline,
			start_time):
		'''
		Create an instance of this object
		'''

		self.session = session
		self.mac_address = mac_address
		self.user = user
		self.pid = pid
		self.program = program
		self.cmdline = cmdline
		self.start_time = start_time



#
# CPL Session
#

class cpl_session:
	'''
	CPL Session
	'''


	def __init__(self, id):
		'''
		Initialize an instance of cpl_session
		'''
		self.id = copy_id(id)


	def __eq__(self, other):
		'''
		Compare this and the other object and return true if they are equal
		'''
		return self.id == other.id


	def __ne__(self, other):
		'''
		Compare this and the other object and return true if they are not equal
		'''
		return self.id != other.id


	def __str__(self):
		'''
		Return a string representation of this object
		'''
		return str(self.id)


	def info(self):
		'''
		Return the cpl_session_info object associated with this session.
		'''

		sessionpp = CPLDirect.new_cpl_session_info_tpp()
		ret = CPLDirect.cpl_get_session_info(self.id,
		    CPLDirect.cpl_convert_pp_cpl_session_info_t(sessionpp))
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_cpl_session_info_tpp(sessionpp)
			raise Exception('Could not find session information: ' +
					CPLDirect.cpl_error_string(ret))

		sessionp = CPLDirect.cpl_dereference_pp_cpl_session_info_t(sessionpp)
		info = CPLDirect.cpl_session_info_tp_value(sessionp)

		_info = cpl_session_info(self, info.mac_address, info.user,
				info.pid, info.program, info.cmdline, info.start_time)
		
		CPLDirect.cpl_free_session_info(sessionp)
		CPLDirect.delete_cpl_session_info_tpp(sessionpp)
		
		return _info



#
# Information about a provenance object
#

class cpl_object_info:
	'''
	Information about a provenance object
	'''

	def __init__(self, object, version, creation_session, creation_time,
			originator, name, type, container):
		'''
		Create an instance of this object
		'''

		self.object = object
		self.version = version
		self.creation_session = creation_session
		self.creation_time = creation_time
		self.originator = originator
		self.name = name
		self.type = type
		self.container = container



#
# CPL Provenance object
#

class cpl_object:
	'''
	CPL Provenance object
	'''


	def __init__(self, id):
		'''
		Create a new instance of a provenance object from its internal ID
		'''
		self.id = copy_id(id)


	def __eq__(self, other):
		'''
		Compare this and the other object and return true if they are equal
		'''
		return self.id == other.id


	def __ne__(self, other):
		'''
		Compare this and the other object and return true if they are not equal
		'''
		return self.id != other.id


	def __str__(self):
		'''
		Return a string representation of this object
		'''
		return str(self.id)


	def version(self):
		'''
		Determine the current version of this provenance object
		'''
		vp = CPLDirect.new_cpl_version_tp()

		ret = CPLDirect.cpl_get_version(self.id, vp)
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_cpl_version_tp(vp)
			raise Exception('Could not determine the version of an object: ' +
					CPLDirect.cpl_error_string(ret))

		v = CPLDirect.cpl_version_tp_value(vp)
		CPLDirect.delete_cpl_version_tp(vp)
		return v


	def new_version(self):
		'''
		Create a new version of this object and return the new version.
		'''
		vp = CPLDirect.new_cpl_version_tp()

		ret = CPLDirect.cpl_new_version(self.id, vp)
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_cpl_version_tp(vp)
			raise Exception('Could not createa a new version of an object: ' +
					CPLDirect.cpl_error_string(ret))

		v = CPLDirect.cpl_version_tp_value(vp)
		CPLDirect.delete_cpl_version_tp(vp)
		return v


	def current_version(self):
		'''
		Get a cpl_object_version object for the current version.
		'''
		return cpl_object_version(self, self.version())


	def specific_version(self, version):
		'''
		Get a cpl_object_version object for the specified version. Note that
		the specified version number does not get validated until info() is
		called.
		'''
		return cpl_object_version(self, version)


	def control_flow_to(self, dest, type=CONTROL_OP, version=None):
		'''
		Add control flow edge of type from self to dest. If version
		is specified, then add flow to dest with explicit version,
		else add to most recent version.

		Allowed types:
			CPL.CONTROL_OP (default)
			CPL.CONTROL_START

		CPL.CONTROL_GENERIC is an alias for CPL.CONTROL_OP.
		'''

		if version is None or version == VERSION_NONE:
			version = self.version()

		ret = CPLDirect.cpl_control_flow_ext(dest.id, self.id, version, type)
		if not CPLDirect.cpl_is_ok(ret):
			raise Exception('Could not add control dependency: ' +
					CPLDirect.cpl_error_string(ret))
		return not ret == S_DUPLICATE_IGNORED


	def data_flow_to(self, dest, type=DATA_INPUT, version=None):
		'''
		Add data flow edge of type from self to dest. If version
		is specified, then add flow to dest with explicit version,
		else add to most recent version.

		Allowed types:
			CPL.DATA_INPUT (default)
			CPL.DATA_IPC
			CPL.DATA_TRANSLATION
			CPL.DATA_COPY

		CPL.DATA_GENERIC is an alias for CPL.DATA_INPUT.
		'''

		if version is None or version == VERSION_NONE:
			version = self.version()

		ret = CPLDirect.cpl_data_flow_ext(dest.id, self.id, version, type)
		if not CPLDirect.cpl_is_ok(ret):
			raise Exception('Could not add data dependency ' +
					CPLDirect.cpl_error_string(ret))
		return not ret == S_DUPLICATE_IGNORED


	def control_flow_from(self, src, type=CONTROL_OP, version=None):
		'''
		Add control flow edge of the given type from src to self. If version
		is specified, then add flow to dest with explicit version, else add
		to most recent version.

		Allowed types:
			CPL.CONTROL_OP (default)
			CPL.CONTROL_START

		CPL.CONTROL_GENERIC is an alias for CPL.CONTROL_OP.
		'''

		if isinstance(src, cpl_object_version):
			if version is not None and version != VERSION_NONE:
				raise Exception('The version argument must be None if ' +
					'src is of type cpl_object_version')
			_version = src.version
			_src = src.object
		elif version is None or version == VERSION_NONE:
			_version = src.version()
			_src = src
		else:
			_version = version
			_src = src

		ret = CPLDirect.cpl_control_flow_ext(self.id, _src.id, _version, type)
		if not CPLDirect.cpl_is_ok(ret):
			raise Exception('Could not add control dependency: ' +
					CPLDirect.cpl_error_string(ret))
		return not ret == S_DUPLICATE_IGNORED


	def data_flow_from(self, src, type=DATA_INPUT, version=None):
		'''
		Add data flow edge of the given type from src to self. If version
		is specified, then add flow to dest with explicit version, else add
		to most recent version.

		Allowed types:
			CPL.DATA_INPUT (default)
			CPL.DATA_IPC
			CPL.DATA_TRANSLATION
			CPL.DATA_COPY

		CPL.DATA_GENERIC is an alias for CPL.DATA_INPUT.
		'''

		if isinstance(src, cpl_object_version):
			if version is not None and version != VERSION_NONE:
				raise Exception('The version argument must be None if ' +
					'src is of type cpl_object_version')
			_version = src.version
			_src = src.object
		elif version is None or version == VERSION_NONE:
			_version = src.version()
			_src = src
		else:
			_version = version
			_src = src

		ret = CPLDirect.cpl_data_flow_ext(self.id, _src.id, _version, type)
		if not CPLDirect.cpl_is_ok(ret):
			raise Exception('Could not add data dependency ' +
					CPLDirect.cpl_error_string(ret))
		return not ret == S_DUPLICATE_IGNORED


	def has_ancestor(self, other):
		'''
		Return True if the other object is an ancestor of the object.
		'''
		ancestors = self.ancestry()
		for a in ancestors:
			if a.ancestor.object == other:
				return True
		return False


	def add_property(self, name, value):
		'''
		Add name/value pair as a property to current object.
		'''
		return CPLDirect.cpl_add_property(self.id, name, value)


	def info(self):
		'''
		Return cpl_object_info_t corresponding to the current object.
		'''
		objectpp = CPLDirect.new_cpl_object_info_tpp()

		ret = CPLDirect.cpl_get_object_info(self.id,
		    CPLDirect.cpl_convert_pp_cpl_object_info_t(objectpp))
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_cpl_object_info_tpp(objectpp)
			raise Exception('Unable to get object info: ' +
					CPLDirect.cpl_error_string(ret))

		op = CPLDirect.cpl_dereference_pp_cpl_object_info_t(objectpp)
		object = CPLDirect.cpl_object_info_tp_value(op)

		if object.container_id == NONE or object.container_version < 0:
			container = None
		else:
			container = cpl_object_version(cpl_object(object.container_id),
					object.container_version)

		_info = cpl_object_info(self, object.version,
				cpl_session(object.creation_session), object.creation_time,
				object.originator, object.name, object.type, container)

		CPLDirect.cpl_free_object_info(op)
		CPLDirect.delete_cpl_object_info_tpp(objectpp)

		return _info


	def ancestry(self, version=None, direction=D_ANCESTORS, flags=0):
		'''
		Return a list of cpl_ancestor objects
		'''
		if version is None:
			version = VERSION_NONE
		vp = CPLDirect.new_std_vector_cpl_ancestry_entry_tp()

		ret = CPLDirect.cpl_get_object_ancestry(self.id, version,
		    direction, flags, CPLDirect.cpl_cb_collect_ancestry_vector, vp)
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_std_vector_cpl_ancestry_entry_tp(vp)
			raise Exception('Error retrieving ancestry: ' +
					CPLDirect.cpl_error_string(ret))
			return None

		v = CPLDirect.cpl_dereference_p_std_vector_cpl_ancestry_entry_t(vp)
		l = []
		if direction == D_ANCESTORS:
			for entry in v:
				a = cpl_ancestor(entry.other_object_id,
					entry.other_object_version,
					entry.query_object_id,
					entry.query_object_version, entry.type, direction)
				l.append(a)
		else:
			for entry in v:
				a = cpl_ancestor(entry.query_object_id,
					entry.query_object_version,
					entry.other_object_id,
					entry.other_object_version, entry.type, direction)
				l.append(a)

		CPLDirect.delete_std_vector_cpl_ancestry_entry_tp(vp)
		return l


	def properties(self, key=None, version=None):
		'''
		Return all the properties associated with the current object.

		If key is set to something other than None, return only those
		properties matching key.

		By default, returns properties for the current version of
		the object, but if version is set to a value other than
		CPL.VERSION_NONE, then will return properties for that version.
		'''
		if version is None:
			version = VERSION_NONE
		vp = CPLDirect.new_std_vector_cplxx_property_entry_tp()

		ret = CPLDirect.cpl_get_properties(self.id, version,
		    key, CPLDirect.cpl_cb_collect_properties_vector, vp)
		if not CPLDirect.cpl_is_ok(ret):
			CPLDirect.delete_std_vector_cplxx_property_entry_tp(vp)
			raise Exception('Error retrieving properties: ' +
					CPLDirect.cpl_error_string(ret))

		v = CPLDirect.cpl_dereference_p_std_vector_cplxx_property_entry_t(vp)
		l = []
		for e in v:
			l.append([e.key, e.value])
		CPLDirect.delete_std_vector_cplxx_property_entry_tp(vp)
		return l

