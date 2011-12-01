/*
 * test-simple.cpp
 * Core Provenance Library
 *
 * Copyright 2011
 *      The President and Fellows of Harvard College.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the University nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE UNIVERSITY OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * Contributor(s): Peter Macko
 */

#include "stdafx.h"
#include "standalone-test.h"


/**
 * Print the cpl_object_info_t structure
 *
 * @param info the info structure
 */
static void
print_object_info(cpl_object_info_t* info)
{
	time_t creation_time = (time_t) info->creation_time;
	char* s_creation_time = ctime(&creation_time);
	if (s_creation_time[strlen(s_creation_time)-1] == '\n') {
		s_creation_time[strlen(s_creation_time)-1] = '\0';
	}

	print(L_DEBUG, "  ID               : %llx:%llx", info->id.hi, info->id.lo);
	print(L_DEBUG, "  Version          : %d", info->version);
	print(L_DEBUG, "  Creation Session : %llx:%llx", info->creation_session.hi,
			                                         info->creation_session.lo);
	print(L_DEBUG, "  Creation Time    : %s", s_creation_time);
	print(L_DEBUG, "  Originator       : %s", info->originator);
	print(L_DEBUG, "  Name             : %s", info->name);
	print(L_DEBUG, "  Type             : %s", info->type);
	print(L_DEBUG, "  Container ID     : %llx:%llx", info->container_id.hi,
			                                         info->container_id.lo);
	print(L_DEBUG, "  Container Version: %d", info->container_version);
}


/**
 * The simplest possible test
 */
void
test_simple(void)
{
	cpl_return_t ret;
	cpl_id_t obj  = CPL_NONE;
	cpl_id_t obj2 = CPL_NONE;
	cpl_id_t obj3 = CPL_NONE;
	cpl_id_t objx;


	// Object creation

	ret = cpl_create_object(ORIGINATOR, "Process A", "Proc", CPL_NONE, &obj);
	print(L_DEBUG, "cpl_create_object --> %llx:%llx [%d]", obj.hi, obj.lo, ret);
	CPL_VERIFY(cpl_create_object, ret);

	ret = cpl_create_object(ORIGINATOR, "Object A", "File", obj, &obj2);
	print(L_DEBUG, "cpl_create_object --> %llx:%llx [%d]", obj2.hi,obj2.lo,ret);
	CPL_VERIFY(cpl_create_object, ret);

	ret = cpl_create_object(ORIGINATOR, "Process B", "Proc", obj, &obj3);
	print(L_DEBUG, "cpl_create_object --> %llx:%llx [%d]", obj3.hi,obj3.lo,ret);
	CPL_VERIFY(cpl_create_object, ret);

	print(L_DEBUG, " ");


	// Object lookup

	ret = cpl_lookup_object(ORIGINATOR, "Process A", "Proc", &objx);
	print(L_DEBUG, "cpl_lookup_object --> %llx:%llx [%d]", objx.hi,objx.lo,ret);
	CPL_VERIFY(cpl_lookup_object, ret);
	if (obj!=objx)throw CPLException("Object lookup returned the wrong object");

	ret = cpl_lookup_object(ORIGINATOR, "Object A", "File", &objx);
	print(L_DEBUG, "cpl_lookup_object --> %llx:%llx [%d]", objx.hi,objx.lo,ret);
	CPL_VERIFY(cpl_lookup_object, ret);
	if(obj2!=objx)throw CPLException("Object lookup returned the wrong object");

	ret = cpl_lookup_object(ORIGINATOR, "Process B", "Proc", &objx);
	print(L_DEBUG, "cpl_lookup_object --> %llx:%llx [%d]", objx.hi,objx.lo,ret);
	CPL_VERIFY(cpl_lookup_object, ret);
	if(obj3!=objx)throw CPLException("Object lookup returned the wrong object");

	print(L_DEBUG, " ");


	// Data and control flow / dependencies

	ret = cpl_data_flow(obj2, obj, CPL_DATA_INPUT);
	print(L_DEBUG, "cpl_data_flow --> %d", ret);
	CPL_VERIFY(cpl_data_flow, ret);

	ret = cpl_data_flow(obj2, obj, CPL_DATA_INPUT);
	print(L_DEBUG, "cpl_data_flow --> %d", ret);
	CPL_VERIFY(cpl_data_flow, ret);

	ret = cpl_control(obj3, obj, CPL_CONTROL_START);
	print(L_DEBUG, "cpl_control --> %d", ret);
	CPL_VERIFY(cpl_control, ret);

	ret = cpl_data_flow_ext(obj, obj3, 0, CPL_DATA_TRANSLATION);
	print(L_DEBUG, "cpl_data_flow_ext --> %d", ret);
	CPL_VERIFY(cpl_data_flow, ret);

	print(L_DEBUG, " ");


	// Object info (assume that the objects were created less than 10 sec. ago)

	cpl_object_info_t* info = NULL;
	cpl_version_t version = CPL_VERSION_NONE;

	ret = cpl_get_version(obj, &version);
	print(L_DEBUG, "cpl_get_version --> %d [%d]", version, ret);
	CPL_VERIFY(cpl_get_version, ret);

	ret = cpl_get_object_info(obj, &info);
	print(L_DEBUG, "cpl_get_object_info --> %d", ret);
	CPL_VERIFY(cpl_get_object_info, ret);

	print_object_info(info);
	if (info->id != obj || info->version != version
			|| info->creation_time > time(NULL)
			|| info->creation_time + 10 < time(NULL)
			|| strcmp(info->originator, ORIGINATOR) != 0
			|| strcmp(info->name, "Process A") != 0
			|| strcmp(info->type, "Proc") != 0
			|| info->container_id != CPL_NONE
			|| info->container_version != CPL_VERSION_NONE) {
		throw CPLException("The returned object information is incorrect");
	}

	ret = cpl_free_object_info(info);
	CPL_VERIFY(cpl_free_object_info, ret);

	print(L_DEBUG, " ");

	ret = cpl_get_version(obj2, &version);
	print(L_DEBUG, "cpl_get_version --> %d [%d]", version, ret);
	CPL_VERIFY(cpl_get_version, ret);

	ret = cpl_get_object_info(obj2, &info);
	print(L_DEBUG, "cpl_get_object_info --> %d", ret);
	CPL_VERIFY(cpl_get_object_info, ret);

	print_object_info(info);
	if (info->id != obj2 || info->version != version
			|| info->creation_time > time(NULL)
			|| info->creation_time + 10 < time(NULL)
			|| strcmp(info->originator, ORIGINATOR) != 0
			|| strcmp(info->name, "Object A") != 0
			|| strcmp(info->type, "File") != 0
			|| info->container_id != obj
			|| info->container_version == CPL_VERSION_NONE) {
		throw CPLException("The returned object information is incorrect");
	}

	ret = cpl_free_object_info(info);
	CPL_VERIFY(cpl_free_object_info, ret);
}
