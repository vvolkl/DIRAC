# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/LoggingSystem/Agent/SystemLoggingDBCleaner.py,v 1.7 2009/10/13 16:34:36 mseco Exp $
__RCSID__ = "$Id: SystemLoggingDBCleaner.py,v 1.7 2009/10/13 16:34:36 mseco Exp $"
"""  SystemLoggingDBCleaner erases records whose messageTime column 
     contains a time older than 'RemoveDate' days, where 'RemoveDate' 
     is an entry in the Configuration Service section of the agent.
"""

from DIRAC.Core.Base.AgentModule import AgentModule
from DIRAC  import S_OK, S_ERROR, gConfig
from DIRAC.ConfigurationSystem.Client.PathFinder import getDatabaseSection
from DIRAC.LoggingSystem.DB.SystemLoggingDB import SystemLoggingDB
from DIRAC.Core.Utilities import dateTime, toString, day


class SystemLoggingDBCleaner(AgentModule):


  def initialize(self):
     
    self.SystemLoggingDB = SystemLoggingDB()
 
    self.period = int( self.am_getOption( "RemoveDate", '30' ) ) * day
    
    return S_OK()	

  def execute(self):
    """ The main agent execution method
    """
    limitDate = toString( dateTime() - self.period )
    limitDate = limitDate[:limitDate.find('.')]

    commonString = 'FROM MessageRepository WHERE messageTime <'
    cmd = "SELECT count(*) %s '%s'" % ( commonString, limitDate )
    result = self.SystemLoggingDB._query( cmd )
    if not result['OK']: 
      return result
    recordsToErase=result['Value'][0][0]

    if recordsToErase == 0:
      self.log.info('No records to erase')
      return S_OK('No records to erase')
    else:
      cmd = "DELETE LOW_PRIORITY %s '%s'" % ( commonString, limitDate )
      result =  self.SystemLoggingDB._update( cmd )
      if not result['OK']:
        self.log.error( 'Could not erase the requested records',
                        'those older than %s' % limitDate )
        return result
      else:
        self.log.info('%s records have been erased' % recordsToErase )
        return result
