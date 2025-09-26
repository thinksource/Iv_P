# 磁盘挂载
2️⃣ 卸载原来的挂载点
umount /tmp/mountd/disk1_part1

    如果提示设备忙，可加 -l 延迟卸载：

umount -l /tmp/mountd/disk1_part1

重新挂载到新路径

假设分区是 NTFS，需要读写支持（已安装 ntfs-3g）：

mount -t ntfs-3g /dev/disk1s1 /tmp/mountd/disk1_part1

如果是 FAT32：

mount -t vfat /dev/sda2 /opt/hdisk

如果是 EXT4：

mount -t ext4 /dev/sda2 /opt/hdisk

    挂载成功后：

ls /opt/hdisk

# 开机自动挂载（可选）

编辑 /etc/config/fstab：

config mount
    option target   '/opt/hdisk'
    option device   '/dev/sda2'
    option fstype   'ntfs-3g'       # 根据实际文件系统改
    option options  'rw,sync'
    option enabled  '1'

重启或运行：

/etc/init.d/fstab restart

即可开机自动挂载到 /opt/hdisk

💡 提示：

ntfs-3g 读写 NTFS，rw,sync 可以确保写入安全

挂载点 /tmp/mountd/disk1_part1 是临时目录，重启后会消失；使用 /opt/hdisk 更持久