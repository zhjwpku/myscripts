#!/bin/bash

if [ 1 -lt $# ]; then
  echo $# + " arguments are too more"
  exit
fi

if [ $# -lt 1 ]; then
  echo $# + " argument is too less"
  exit
fi

secure=$1

QEMU=/bin/qemu-kvm
IMAGES=/root/ubuntu14.img
VDAGENT_PARAM="-device virtio-serial-pci,id=virtio-serial0,bus=pci.0,addr=0x10 \
-chardev spicevmc,id=charchannel0,name=vdagent -device virtserialport,bus=virtio-serial0.0,nr=1,chardev=charchannel0,id=channel0,name=com.redhat.spice.0"
BIOS_PARAM="-bios bios.bin"

#$QEMU $BIOS_PARAM -m 1024 -drive file=$IMAGES,if=none,id=drive-ide0-0-0,format=raw,cache=none -device ide-hd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=1 -drive if=none,id=drive-ide0-1-0,readonly=on,format=raw 
#-vnc :1 -spice port=7001,disable-ticketing -enable-kvm -smp 1 $USB_PARAM -usbdevice tablet -soundhw all --full-screen -monitor stdio -vga qxl -global qxl-vga.ram_size=67108865 -global qxl-vga.vram_size=67108864 $VDAGENT_PARAM

#$QEMU $BIOS_PARAM -m 2048 -drive file=$IMAGES,if=none,id=drive-ide0-0-0,format=raw,cache=none -device ide-hd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=1 -drive if=none,id=drive-ide0-1-0,readonly=on,format=raw -spice port=7001,disable-ticketing -enable-kvm -smp 2 $USB_PARAM -usbdevice tablet -soundhw all --full-screen -monitor stdio -vga qxl -global qxl-vga.ram_size=67108865 -global qxl-vga.vram_size=67108864 $VDAGENT_PARAM

#$QEMU -m 2048 -drive file=$IMAGES,if=none,id=drive-ide0-0-0,format=raw,cache=none -device ide-hd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=1 -enable-kvm -smp 4 -monitor stdio -vga qxl -spice port=7001,disable-ticketing -device virtio-serial-pci,id=virtio-serial0,bus=pci.0,addr=0x6 -chardev pty,id=charserial0 -device isa-serial,chardev=charserial0,id=serial0 -chardev spicevmc,id=charchannel0,name=vdagent -device virtserialport,bus=virtio-serial0.0,nr=1,chardev=charchannel0,id=channel0,name=com.redhat.spice.0 -device usb-tablet,id=input0 $USB_PARAM

#$QEMU $BIOS_PARAM -name ubuntu14 -m 2048 -smp 1 -enable-kvm -soundhw all -monitor stdio --full-screen -vga qxl -global qxl-vga.ram_size=67108864 -global qxl-vga.vram_size=67108864 -spice port=3001,disable-ticketing ubuntu14.img $VDAGENT_PARAM

if [ $secure = "1" ]; then 
  echo "tls-port 5901"
  $QEMU $BIOS_PARAM -name ubuntu14 -m 2048 -smp 1 -enable-kvm -soundhw all -monitor stdio --full-screen -vga qxl -global qxl-vga.ram_size=67108864 -global qxl-vga.vram_size=67108864 -spice tls-port=5901,disable-ticketing,x509-dir=./ ubuntu14.img $VDAGENT_PARAM
else
  echo "port 3001"
  $QEMU $BIOS_PARAM -name ubuntu14 -m 2048 -smp 1 -enable-kvm -soundhw all -monitor stdio --full-screen -vga qxl -global qxl-vga.ram_size=67108864 -global qxl-vga.vram_size=67108864 -spice port=3001,disable-ticketing,x509-dir=./ ubuntu14.img $VDAGENT_PARAM
fi
