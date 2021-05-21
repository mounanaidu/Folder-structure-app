from addfile import add
from view import viewroot, view, printView
from delete import delete
from filterData import filterData, printFilter

if __name__ == '__main__':
    while True:
        command = input("Enter your command: ").strip(' ')
        c = command.split(' ')
        del_c = command.split(' ',1)

        if c[0] == 'add':
            add(c[1])
        elif c[0] == 'view':
            if len(c)>1:
                resultDict = view(c[1], {})
                printView(resultDict, 0)
            else:
                viewroot()
        elif del_c[0] == 'delete':
            delete(del_c[1])
        elif c[0] == 'filter':
            folder = c[1]
            column = c[2]
            value = c[3]
            resultDict = filterData(folder, {}, column, value)
            printFilter(resultDict, 0)
        elif c[0] == 'exit':
            print("See you!")
            break
        else:
            print("Incorrect command")
