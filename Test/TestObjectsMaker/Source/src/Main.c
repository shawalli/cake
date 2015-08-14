
#include <stdio.h>
#include <TestApp_Globals.h>

int
main(void)
{
    printf("Hello World!\n");

    if (0 != TestApp_gText)
    {
        printf("text(%s)\n");
    }

    return 0;
}
