#include <stdio.h>
#include <stdlib.h>

int main()
{
FILE *in;
char a;
in=fopen("file.txt", "rt");
if(in==0){
printf("No file of such\n");
return 1;
}

while(1){
a = fgetc(in);
if(a >= 'A' && a <= 'Z')
printf("%c", a);
if(a==EOF) break;
}
printf("\n");
fclose(in);

return 0;

}
