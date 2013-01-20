#include <stdio.h>

void lgsm(int *pa, int *pb, int array[10]){
int i;
*pa = array[0];
*pb = array[0];

for(i=0; i<10; i++){
if(array[i] > *pa) *pa = array[i];
if(array[i] < *pb) *pb = array[i];
}

}

int main(){
int m=0, n=0, store[10], i;

for(i=0; i<10; i++){
printf("Input a number: ");
scanf("%d", &store[i]);

}

lgsm(&m, &n, store);

printf("The largest no is %d and the smallest is %d\n", m, n);

return 0;

}
