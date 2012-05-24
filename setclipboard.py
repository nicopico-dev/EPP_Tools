import win32clipboard as w
import optparse

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-t","--text",action="store",type="string",dest="text",help="Text to be copied to the clipboard")
    
    parser.set_defaults()
    (options, args) = parser.parse_args()
    
    if options.text:
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardText(options.text)
        w.CloseClipboard()
        
    else: 
        # Provoquer une erreur
        parser.print_help()
        sys.exit(1)