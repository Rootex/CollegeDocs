#include <stdio.h>

int logical(int number){
if(number > 10){
printf("True\n");
return 1;
}
else{
printf("False\n");
return 0;
}
}
main(){
int a;

printf("Enter a number: ");
scanf("%d", &a);

logical(a);

}
