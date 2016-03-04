/*
 * @author: Zhao Junwang
 * @email: zhjwpku@gmai.com
 * @usage: ./read addr
 */

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define MEM1_SIZE	4096

int main(int argc, char *argv[])
{
	int ret = 0;
	int fd = -1;
	unsigned int val = 0;
	unsigned int reg_base = 0;

	unsigned int addr = 0;
	unsigned int offset = 0;

	if (argc != 2) {
		printf("bad args ! exp: ./read 0xc0c00000\n");
		printf("[0xc0c00000] = 0x44453286\n");
		return -1;
	}

	sscanf(argv[1], "%x", &val);
	printf("read 0x%8.8x\n", val);

	offset = val % 4096;
	addr = val - offset;

	fd = open("/dev/mem", O_RDWR | O_SYNC);
	if (fd < 0) {
		fprintf(stderr, "cannot open /dev/mem\n");
		return -1;
	}

	reg_base = (unsigned int) mmap(NULL, MEM1_SIZE, PROT_READ | PROT_WRITE |MAP_FIXED,
			MAP_SHARED, fd, addr);

	if (reg_base == (unsigned int)MAP_FAILED) {
		reg_base = 0;
		fprintf(stderr, "mmmap mem1 error\n");
		close(fd);
		return -1;
	}

	int i;

	for(i = 0; i < 36; i++) {
		if(i % 4 == 3)
			printf("[0x%8.8x] = 0x%8.8x\n",val + 4 * i , *((unsigned int *)(reg_base + offset) + i));
		else
			printf("[0x%8.8x] = 0x%8.8x  ",val + 4 * i , *((unsigned int *)(reg_base + offset) + i));
	}

here_exit:
	if (reg_base)
		ret = munmap((void *)reg_base, MEM1_SIZE);

	if(fd>0)
		close(fd);
	return 0;
}
