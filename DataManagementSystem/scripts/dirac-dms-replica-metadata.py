#!/usr/bin/env python
########################################################################
# $HeadURL$
########################################################################
__RCSID__   = "$Id$"

from DIRAC.Core.Base import Script 

Script.setUsageMessage("""
Get the given file replica metadata from the File Catalog

Usage:
   %s <LFN | fileContainingLFNs> SE 
""" % Script.scriptName)

Script.parseCommandLine()

from DIRAC import gLogger
from DIRAC.DataManagementSystem.Client.ReplicaManager import ReplicaManager
import os, sys

if not len( sys.argv ) == 3:
  Script.showHelp()
  DIRAC.exit( -1 )
else:
  inputFileName = sys.argv[1]
  storageElement = sys.argv[2]

if os.path.exists( inputFileName ):
  inputFile = open( inputFileName, 'r' )
  string = inputFile.read()
  lfns = string.splitlines()
  inputFile.close()
else:
  lfns = [inputFileName]

rm = ReplicaManager()
res = rm.getReplicaMetadata( lfns, storageElement )
if not res['OK']:
  print 'Error:',res['Message']
  sys.exit(1)
  
print '%s %s %s %s' % ( 'File'.ljust( 100 ), 'Migrated'.ljust( 8 ), 'Cached'.ljust( 8 ), 'Size (bytes)'.ljust( 10 ) )
for lfn, metadata in res['Value']['Successful'].items():
  print '%s %s %s %s' % ( lfn.ljust( 100 ), str( metadata['Migrated'] ).ljust( 8 ), str( metadata['Cached'] ).ljust( 8 ), str( metadata['Size'] ).ljust( 10 ) )
for lfn, reason in res['Value']['Failed'].items():
  print '%s %s' % ( lfn.ljust( 100 ), reason.ljust( 8 ) )
