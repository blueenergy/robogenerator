from pyparsing import *

header='''
documentation ='The case is to test ##title##'

output_filename ='##title##.html'
case_name_template = '##title##'

'''


division = Suppress(":")
words = Word(alphanums)
startBody,endBody = makeHTMLTags("body")
startH1,endH1 = makeHTMLTags("h1")
startH1.setParseAction( withAttribute(align="center") )
anchorS,anchorE = makeHTMLTags("A")
startH2,endH2 = makeHTMLTags("h2")
startH3,endH3 = makeHTMLTags("h3")
keyword = words+ZeroOrMore(' ')+ZeroOrMore(words)
keyword.setParseAction(lambda t:' '.join(t))
content = keyword.setResultsName('action')+ZeroOrMore(division)+ZeroOrMore(keyword).setResultsName('expected_result')
content.setParseAction(lambda p:(p.action,p.expected_result))
content.setResultsName('content')


title_template = Suppress(startH1)+Suppress(anchorS)+keyword+Suppress(anchorE)+Suppress(endH1)
title_template.setResultsName('title')

def parse_action(t):
    if t[0][1]:
        return (t[0][0],t[0][1][0])
    else:
        return (t[0][0],'')
action = Suppress(startH3)+Suppress(anchorS)+content+Suppress(anchorE)+Suppress(endH3)
action.setParseAction(parse_action)
action.setResultsName('action')

state_name = Suppress(startH2)+Suppress(anchorS)+keyword+Suppress(anchorE)+Suppress(endH2)
state_name.setParseAction(lambda t: t[0])
state_name.setResultsName('state_name')

state = state_name.setResultsName('state_name')+OneOrMore(action).setResultsName('actions')
state.setParseAction(lambda p: (p.state_name,list(p.actions)))
state.setResultsName('state')


states_template = OneOrMore(state).setResultsName('states')
html = startBody+states_template+endBody



def main():
    import argparse
    global title,states
    parser = argparse.ArgumentParser(description='Robomind 0.1 - a too to convert xmind html file to Robot Cases',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input', type=str, help='input file')
    '''
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='output file (default is input file with NEW prefix)')
    '''
    args = parser.parse_args()
    
    input = args.input
    #output = args.output
    output_filename = input.split('.')[0]+'_'+'case'
    raw_output = output_filename + '.' + 'txt'
    
    with open(input,'r') as f:
        html_doc= f.read()

    html_doc = html_doc.replace(',',' ')
    for srvrtokens,startloc,endloc in title_template.scanString(html_doc):
        title = srvrtokens[0]
        
    print title
    
    for srvrtokens,startloc,endloc in states_template.scanString(html_doc):
        states = srvrtokens
        print states
        print '**********'
    
    
    with open(raw_output,'w') as f:
        f.write(header.replace('##title##',title))
        f.write('*** Test Cases ***\n')
        index=1
        for state in states:
            for action in state[1]:
                f.write('Test%s\n'%index)
                f.write('  Given %s\n'%state[0])
                f.write('  When %s\n'%action[0])
                if action[1]:
                    f.write('  Then %s\n'%action[1])
                index +=1

    from tidy import tidy_cli

    command_string = '--inplace --format %s %s' % ('html', raw_output) #print command_string
    command_string_list = command_string.split(' ') 

    retcode = tidy_cli(command_string_list)


if __name__=='__main__':
    main()
