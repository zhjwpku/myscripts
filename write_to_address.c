/*
 * @author: Zhao Junwang
 * @email: zhjwpku@gmai.com
 * @usage: ./write addr val
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

	unsigned int addr_ori = 0;
	unsigned int addr = 0;
	unsigned int offset = 0;

	if (argc != 3) {
		printf("bad args ! exp: ./write 0xee800008 0x11111111\n");
		return -1;
	}

	sscanf(argv[1], "%x", &addr_ori);
	sscanf(argv[2], "%x", &val);
	printf("write 0x%8.8x to 0x%8.8x\n", val, addr_ori);

	offset = addr_ori % 4096;
	addr = addr_ori - offset;

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

	*((unsigned int *)(reg_base + offset)) = val;

	printf("[0x%8.8x] = 0x%8.8x\n",addr_ori , *((unsigned int *)(reg_base + offset)));

here_exit:
	if (reg_base)
		ret = munmap((void *)reg_base, MEM1_SIZE);

	if(fd>0)
		close(fd);
	return 0;
}
