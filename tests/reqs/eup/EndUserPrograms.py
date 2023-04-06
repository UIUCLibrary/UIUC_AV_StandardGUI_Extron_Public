from services import EndUserPrograms_impl as eup
EUP_VERSION = eup.getVersion()
EUP_PLATFORM = eup.getPlatform()

if __name__ == '__main__':
    import argparse
    eup.setup()
    parser = argparse.ArgumentParser()
    eup.addArgs(parser)
    args = parser.parse_args()
    if args.debug:
        import Extron3.SysSrv
        Extron3.SysSrv.Enabledebug()

        import services.Extronrpdb2
        services.Extronrpdb2.start_embedded_debugger('pass', timeout=None)      
        eup.debugInitStatus = True                
            
    eup.runEup(args)
