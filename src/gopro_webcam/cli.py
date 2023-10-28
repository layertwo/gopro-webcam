from gopro_webcam import GoProWebcam

def main():
    ip = IPv4Address("172.22.100.51")
    gp = GoProWebcam(ip=ip)
    gp.start()
    # gp.set_resolution(resolution=Resolution.FHD)
    # gp.set_fov(fov=Fov.WIDE)
    gp.stop()
    # gp.sleep()
    # gp.get_status()


if __name__ == "__main__":
    main()
