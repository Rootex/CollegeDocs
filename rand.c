#include <stdio.h>

int great(int array[10]){
int i;

for(i=0; i<10; i++){
if(array[i] > 10)
printf("%d\n", array[i]);
}


}

int main()
{
int store[10], i;
for(i=0; i<10; i++)
store[i] = rand()%101;

great(store);

return 0; 

}
