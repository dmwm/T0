"""
_ConfDB_

Interfaces to ConfDB

"""
import os
import logging

from WMCore.DAOFactory import DAOFactory
from WMCore.Database.DBFactory import DBFactory
from WMCore.Configuration import loadConfigurationFile


def getConfiguration(hltkey):
    """
    _getConfiguration_

    Query ConfDB with the HLT configuration name for the
    details of streams, primary datasets and trigger paths.

    Return None in case of problems and let the caller deal with it

    """

    logging.info("Trying to retrieve configuration for hltkey %s" % hltkey)

    if not os.environ.has_key('WMAGENT_CONFIG'):
        logging.error("You do not have WMAGENT_CONFIG in your environment !")
        return None

    wmAgentConfig = loadConfigurationFile(os.environ["WMAGENT_CONFIG"])

    if not hasattr(wmAgentConfig, "HLTConfDatabase"):
        logging.error("Your config is missing the HLTConfDatabase section !")
        return None

    connectUrl = getattr(wmAgentConfig.HLTConfDatabase, "connectUrl", None)

    dbFactory = DBFactory(logging, dburl = connectUrl, options = {})
    dbInterface = dbFactory.connect()

    daoFactory = DAOFactory(package = "T0.WMBS",
                            logger = logging,
                            dbinterface = dbInterface)

    getHLTConfigDAO = daoFactory(classname = "RunConfig.GetHLTConfig")
    hltConfig = getHLTConfigDAO.execute(hltkey)

    if hltConfig['process'] == None or len(hltConfig['mapping']) == 0:
        logging.error("HLT Configuration is empty !")
        return None
    else:
        return hltConfig
