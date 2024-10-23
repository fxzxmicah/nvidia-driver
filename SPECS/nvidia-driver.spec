%define kernel_ver %(rpm -q --qf "%%{VERSION}-%%{RELEASE}" kernel-devel)

Name:               nvidia-driver
Version:            560.35.03
Release:            1%{?dist}
Summary:            NVIDIA binary driver for Linux
License:            NVIDIA
URL:                http://www.nvidia.com/
Source0:            https://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-no-compat32.run
Source1:            https://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-no-compat32.run.sha256sum
Source2:            nvidia-modsign-key-ABE56D9A.key
Source3:            nvidia-modsign-crt-ABE56D9A.der

BuildRequires:      gcc
BuildRequires:      make
BuildRequires:      kernel-devel
BuildRequires:      openssl
BuildRequires:      systemd-rpm-macros

Requires:           kernel = %{kernel_ver}
Requires:           nvidia-modules = %{version}-%{release}

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
The NVIDIA Linux graphics driver.

%package -n nvidia-modules
Summary:            NVIDIA kernel modules
Group:              System Environment/Kernel

%description -n nvidia-modules
NVIDIA Linux graphics kernel modules

%package -n nvidia-wayland
Summary:            NVIDIA Wayland libraries

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-wayland
NVIDIA Wayland libraries

%package -n nvidia-gbm
Summary:            NVIDIA GBM libraries

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-gbm
NVIDIA GBM libraries

%package -n nvidia-opencl
Summary:            NVIDIA OpenCL libraries

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-opencl
NVIDIA OpenCL libraries

%package -n nvidia-cuda
Summary:            NVIDIA CUDA libraries

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-cuda
NVIDIA CUDA libraries

%package -n nvidia-vision
Summary:            NVIDIA Vision libraries

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-vision
NVIDIA Vision libraries

%package -n nvidia-vdpau
Summary:            NVIDIA VDPAU libraries

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-vdpau
NVIDIA VDPAU libraries

%package -n nvidia-persistenced
Summary:            NVIDIA Persistenced Utilities

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-persistenced
NVIDIA Persistenced Utilities

%package -n nvidia-powerd
Summary:            NVIDIA Powerd Utilities

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-powerd
NVIDIA Powerd Utilities

%package -n nvidia-settings
Summary:            NVIDIA Settings Application

Requires:           %{name} = %{version}-%{release}

Requires:           dbus

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description -n nvidia-settings
NVIDIA Settings Application

%package -n nvidia-X
Summary:            NVIDIA X drivers

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-X
NVIDIA X drivers

%package -n nvidia-ngx
Summary:            NVIDIA NGX Utilities

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-ngx
NVIDIA NGX Utilities

%package -n nvidia-security
Summary:            NVIDIA Security Libraries

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-security
NVIDIA Security Libraries

%package -n nvidia-utils
Summary:            NVIDIA Utilities

Requires:           %{name} = %{version}-%{release}

%description -n nvidia-utils
NVIDIA Utilities

%package -n nvidia-devel
Summary:            NVIDIA Development Files

%description -n nvidia-devel
NVIDIA Development Files

%prep
cd %{_sourcedir}
#verify sha256sum
sha256sum -c NVIDIA-Linux-x86_64-%{version}-no-compat32.run.sha256sum
sh %{Source0} --extract-only --target %{_builddir}/%{name}-%{version}
mkdir -p %{buildroot}%{_prefix}/src
cp -r %{_builddir}/%{name}-%{version}/kernel %{buildroot}%{_prefix}/src/nvidia-%{version}

%build
cd %{_builddir}/%{name}-%{version}
export KERNEL_UNAME=%{kernel_ver}.%{_arch}
export NV_EXCLUDE_KERNEL_MODULES="nvidia-vgpu-vfio nvidia-peermem"
%{make_build} modules

%install
cd %{_builddir}/%{name}-%{version}

%{_prefix}/src/kernels/%{kernel_ver}.%{_arch}/scripts/sign-file sha256 %{Source2} %{Source3} *.ko

mkdir -p %{buildroot}/lib/firmware/nvidia/%{version}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}-sleep
mkdir -p %{buildroot}%{_prefix}/lib/nvidia
mkdir -p %{buildroot}%{_libdir}/nvidia
mkdir -p %{buildroot}%{_sysconfdir}/OpenCL/vendors
mkdir -p %{buildroot}%{_datadir}/dbus-1/system.d
mkdir -p %{buildroot}%{_sysconfdir}/vulkan/icd.d
mkdir -p %{buildroot}%{_sysconfdir}/vulkan/implicit_layer.d
mkdir -p %{buildroot}%{_datadir}/nvidia
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_libdir}/xorg/modules/extensions
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d
mkdir -p %{buildroot}%{_libdir}/xorg/modules/drivers
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}%{_libdir}/vdpau
mkdir -p %{buildroot}/lib/modules/%{kernel_ver}.%{_arch}/kernel/drivers/video
mkdir -p %{buildroot}%{_datadir}/applications

mv firmware/* %{buildroot}/lib/firmware/nvidia/%{version}
mv nvidia-bug-report.sh %{buildroot}%{_bindir}
mv nvidia-modprobe %{buildroot}%{_bindir}
mv nvidia-modprobe.1.gz %{buildroot}%{_mandir}/man1
mv systemd/system/* %{buildroot}%{_unitdir}
mv systemd/system-sleep/* %{buildroot}%{_unitdir}-sleep
mv systemd/nvidia-sleep.sh %{buildroot}%{_bindir}
mv libglvnd_install_checker/* %{buildroot}/usr/lib/nvidia
mv nvidia-smi %{buildroot}%{_bindir}
mv nvidia-smi.1.gz %{buildroot}%{_mandir}/man1
mv libnvidia-ml.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia-debugdump %{buildroot}%{_bindir}
mv libcuda.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-opencl.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libOpenCL.so.* %{buildroot}%{_libdir}/nvidia
mv nvidia.icd %{buildroot}%{_sysconfdir}/OpenCL/vendors
mv nvidia-cuda-mps-control %{buildroot}%{_bindir}
mv nvidia-cuda-mps-server %{buildroot}%{_bindir}
mv nvidia-cuda-mps-control.1.gz %{buildroot}%{_mandir}/man1
mv libnvidia-ptxjitcompiler.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libcudadebugger.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia-persistenced.1.gz %{buildroot}%{_mandir}/man1
mv nvidia-persistenced %{buildroot}%{_bindir}
mv libnvidia-nvvm.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-gpucomp.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-api.so.* %{buildroot}%{_libdir}/nvidia
mv nvidia-powerd %{buildroot}%{_bindir}
mv nvidia-dbus.conf %{buildroot}%{_datadir}/dbus-1/system.d
mv libnvidia-glcore.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-tls.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia_icd.json %{buildroot}%{_sysconfdir}/vulkan/icd.d
mv nvidia_layers.json %{buildroot}%{_sysconfdir}/vulkan/implicit_layer.d
mv nvidia-application-profiles-%{version}-* %{_datadir}/nvidia
mv libGLX_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-glsi.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-glvkspirv.so.%{version} %{buildroot}%{_libdir}/nvidia
mv 10_nvidia.json %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mv libglxserver_nvidia.so.%{version} %{buildroot}%{_libdir}/xorg/modules/extensions
mv libnvidia-eglcore.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libEGL_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libGLESv2_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libGLESv1_CM_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-egl-wayland.so.* %{buildroot}%{_libdir}/nvidia
mv 10_nvidia_wayland.json %{buildroot}%{_datadir}/egl/egl_external_platform.d
mv libnvidia-egl-gbm.so.* %{buildroot}%{_libdir}/nvidia
mv 15_nvidia_gbm.json %{buildroot}%{_datadir}/egl/egl_external_platform.d
mv nvidia_drv.so %{buildroot}%{_libdir}/xorg/modules/drivers
mv nvidia-settings.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mv nvidia-xconfig %{buildroot}%{_bindir}
mv nvidia-xconfig.1.gz %{buildroot}%{_mandir}/man1
mv nvidia-settings %{buildroot}%{_bindir}
mv libnvidia-gtk2.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-gtk3.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-wayland-client.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia-settings.1.gz %{buildroot}%{_mandir}/man1
mv libnvidia-cfg.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libvdpau_nvidia.so.%{version} %{buildroot}%{_libdir}/vdpau
mv libnvidia-allocator.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-rtcore.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvoptix.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvoptix.bin %{buildroot}%{_datadir}/nvidia
mv libnvidia-ngx.so.%{version} %{buildroot}%{_libdir}/nvidia
mv nvidia-ngx-updater %{buildroot}%{_bindir}
mv libnvidia-fbc.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvcuvid.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-encode.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-opticalflow.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-pkcs11.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-pkcs11-openssl3.so.%{version} %{buildroot}%{_libdir}/nvidia
mv kernel/*.ko %{buildroot}/lib/modules/%{kernel_ver}.%{_arch}/kernel/drivers/video
mv nvidia-settings.desktop %{buildroot}%{_datadir}/applications

cp -r %{Source3} %{buildroot}%{_datadir}/nvidia

# Create symbolic links
cd %{buildroot}%{_libdir}
ln -sr nvidia/libnvidia-ml.so.%{version} libnvidia-ml.so.1
ln -sr libnvidia-ml.so.1 libnvidia-ml.so
ln -sr nvidia/libcuda.so.%{version} libcuda.so.1
ln -sr libcuda.so.1 libcuda.so
ln -sr nvidia/libnvidia-opencl.so.%{version} libnvidia-opencl.so.1
ln -sr nvidia/libOpenCL.so.* libOpenCL.so.1
ln -sr libOpenCL.so.1 libOpenCL.so
ln -sr nvidia/libnvidia-ptxjitcompiler.so.%{version} libnvidia-ptxjitcompiler.so.1
ln -sr libnvidia-ptxjitcompiler.so.1 libnvidia-ptxjitcompiler.so
ln -sr nvidia/libcudadebugger.so.%{version} libcudadebugger.so.1
ln -sr nvidia/libnvidia-nvvm.so.%{version} libnvidia-nvvm.so.4
ln -sr libnvidia-nvvm.so.4 libnvidia-nvvm.so
ln -sr nvidia/libnvidia-gpucomp.so.%{version} libnvidia-gpucomp.so.1
ln -sr nvidia/libnvidia-api.so.* libnvidia-api.so.1
ln -sr nvidia/libnvidia-glcore.so.%{version} libnvidia-glcore.so.1
ln -sr nvidia/libnvidia-tls.so.%{version} libnvidia-tls.so.1
ln -sr nvidia/libGLX_nvidia.so.%{version} libGLX_nvidia.so.0
ln -sr nvidia/libnvidia-glsi.so.%{version} libnvidia-glsi.so.1
ln -sr nvidia/libnvidia-glvkspirv.so.%{version} libnvidia-glvkspirv.so.1
ln -sr xorg/modules/extensions/libglxserver_nvidia.so.%{version} xorg/modules/extensions/libglxserver_nvidia.so
ln -sr nvidia/libnvidia-eglcore.so.%{version} libnvidia-eglcore.so.1
ln -sr nvidia/libEGL_nvidia.so.%{version} libEGL_nvidia.so.0
ln -sr nvidia/libGLESv2_nvidia.so.%{version} libGLESv2_nvidia.so.2
ln -sr nvidia/libGLESv1_CM_nvidia.so.%{version} libGLESv1_CM_nvidia.so.1
ln -sr nvidia/libnvidia-egl-wayland.so.* libnvidia-egl-wayland.so.1
ln -sr nvidia/libnvidia-egl-gbm.so.* libnvidia-egl-gbm.so.1
ln -sr nvidia/libnvidia-gtk2.so.%{version} libnvidia-gtk2.so.0
ln -sr nvidia/libnvidia-gtk3.so.%{version} libnvidia-gtk3.so.0
ln -sr nvidia/libnvidia-wayland-client.so.%{version} libnvidia-wayland-client.so.0
ln -sr nvidia/libnvidia-cfg.so.%{version} libnvidia-cfg.so.1
ln -sr libnvidia-cfg.so.1 libnvidia-cfg.so
ln -sr nvidia/vdpau/libvdpau_nvidia.so.%{version} nvidia/vdpau/libvdpau_nvidia.so.1
ln -sr nvidia/vdpau/libvdpau_nvidia.so.1 libvdpau_nvidia.so
ln -sr nvidia/libnvidia-allocator.so.%{version} libnvidia-allocator.so.1
ln -sr libnvidia-allocator.so.1 libnvidia-allocator.so
ln -sr nvidia/libnvidia-rtcore.so.%{version} libnvidia-rtcore.so.1
ln -sr nvidia/libnvoptix.so.%{version} libnvoptix.so.1
ln -sr nvidia/libnvidia-ngx.so.%{version} libnvidia-ngx.so.1
ln -sr nvidia/libnvidia-fbc.so.%{version} libnvidia-fbc.so.1
ln -sr libnvidia-fbc.so.1 libnvidia-fbc.so
ln -sr nvidia/libnvcuvid.so.%{version} libnvcuvid.so.1
ln -sr libnvcuvid.so.1 libnvcuvid.so
ln -sr nvidia/libnvidia-encode.so.%{version} libnvidia-encode.so.1
ln -sr libnvidia-encode.so.1 libnvidia-encode.so
ln -sr nvidia/libnvidia-opticalflow.so.%{version} libnvidia-opticalflow.so.1
ln -sr libnvidia-opticalflow.so.1 libnvidia-opticalflow.so
ln -sr nvidia/libnvidia-pkcs11.so.%{version} libnvidia-pkcs11.so.1
ln -sr nvidia/libnvidia-pkcs11-openssl3.so.%{version} libnvidia-pkcs11-openssl3.so.1

%post
%systemd_post nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service

%post -n nvidia-powerd
%systemd_post nvidia-powerd.service

%post -n nvidia-modules
/sbin/depmod -a

%preun
%systemd_preun nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service

%preun -n nvidia-powerd
%systemd_preun nvidia-powerd.service

%postun
%systemd_postun nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service

%postun -n nvidia-powerd
%systemd_postun nvidia-powerd.service

%postun -n nvidia-modules
/sbin/depmod -a

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.txt
%doc NVIDIA_Changelog
%doc html/
%doc supported-gpus/
%{_bindir}/nvidia-modprobe
%{_bindir}/nvidia-sleep.sh
%{_bindir}/nvidia-smi
%dir %{_libdir}/nvidia
%{_libdir}/nvidia/libnvidia-ml.so.%{version}
%{_libdir}/libnvidia-ml.so.1
%{_libdir}/libnvidia-ml.so
%{_libdir}/nvidia/libnvidia-gpucomp.so.%{version}
%{_libdir}/libnvidia-gpucomp.so.1
%{_libdir}/nvidia/libnvidia-api.so.*
%{_libdir}/libnvidia-api.so.1
%{_libdir}/nvidia/libnvidia-glcore.so.%{version}
%{_libdir}/libnvidia-glcore.so.1
%{_libdir}/nvidia/libnvidia-tls.so.%{version}
%{_libdir}/libnvidia-tls.so.1
%{_libdir}/nvidia/libGLX_nvidia.so.%{version}
%{_libdir}/libGLX_nvidia.so.0
%{_libdir}/nvidia/libnvidia-glsi.so.%{version}
%{_libdir}/libnvidia-glsi.so.1
%{_libdir}/nvidia/libnvidia-glvkspirv.so.%{version}
%{_libdir}/libnvidia-glvkspirv.so.1
%{_libdir}/nvidia/libnvidia-eglcore.so.%{version}
%{_libdir}/libnvidia-eglcore.so.1
%{_libdir}/nvidia/libEGL_nvidia.so.%{version}
%{_libdir}/libEGL_nvidia.so.0
%{_libdir}/nvidia/libGLESv2_nvidia.so.%{version}
%{_libdir}/libGLESv2_nvidia.so.2
%{_libdir}/nvidia/libGLESv1_CM_nvidia.so.%{version}
%{_libdir}/libGLESv1_CM_nvidia.so.1
%{_libdir}/nvidia/libnvidia-cfg.so.%{version}
%{_libdir}/libnvidia-cfg.so.1
%{_libdir}/libnvidia-cfg.so
%{_libdir}/nvidia/libnvidia-allocator.so.%{version}
%{_libdir}/libnvidia-allocator.so.1
%{_libdir}/libnvidia-allocator.so
%{_unitdir}/nvidia-suspend.service
%{_unitdir}/nvidia-hibernate.service
%{_unitdir}/nvidia-resume.service
%{_unitdir}-sleep/nvidia
%{_sysconfdir}/vulkan/icd.d/nvidia_icd.json
%{_sysconfdir}/vulkan/implicit_layer.d/nvidia_layers.json
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-*
%{_datadir}/glvnd/egl_vendor.d/*
%{_mandir}/man1/nvidia-modprobe.1.gz
%{_mandir}/man1/nvidia-smi.1.gz

%files -n nvidia-modules
%defattr(-,root,root,-)
%dir /lib/firmware/nvidia/%{version}
/lib/firmware/nvidia/%{version}/*
/lib/modules/%{kernel_ver}.%{_arch}/kernel/drivers/video/*
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-modsign-*.der

%files -n nvidia-wayland
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-egl-wayland.so.*
%{_libdir}/libnvidia-egl-wayland.so.1
%{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json

%files -n nvidia-gbm
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-egl-gbm.so.*
%{_libdir}/libnvidia-egl-gbm.so.1
%{_datadir}/egl/egl_external_platform.d/15_nvidia_gbm.json

%files -n nvidia-opencl
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-opencl.so.%{version}
%{_libdir}/libnvidia-opencl.so.1
%{_libdir}/nvidia/libOpenCL.so.*
%{_libdir}/libOpenCL.so.1
%{_libdir}/libOpenCL.so
%{_sysconfdir}/OpenCL/vendors/nvidia.icd

%files -n nvidia-cuda
%defattr(-,root,root,-)
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_libdir}/nvidia/libcuda.so.%{version}
%{_libdir}/libcuda.so.1
%{_libdir}/libcuda.so
%{_libdir}/nvidia/libnvidia-ptxjitcompiler.so.%{version}
%{_libdir}/libnvidia-ptxjitcompiler.so.1
%{_libdir}/libnvidia-ptxjitcompiler.so
%{_libdir}/nvidia/libcudadebugger.so.%{version}
%{_libdir}/libcudadebugger.so.1
%{_libdir}/nvidia/libnvidia-nvvm.so.%{version}
%{_libdir}/libnvidia-nvvm.so.1
%{_libdir}/libnvidia-nvvm.so
%{_mandir}/man1/nvidia-cuda-mps-control.1.gz
%{_mandir}/man1/nvidia-cuda-mps-server.1.gz

%files -n nvidia-vision
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-rtcore.so.%{version}
%{_libdir}/libnvidia-rtcore.so.1
%{_libdir}/nvidia/libnvoptix.so.%{version}
%{_libdir}/libnvoptix.so.1
%{_libdir}/nvidia/libnvcuvid.so.%{version}
%{_libdir}/libnvcuvid.so.1
%{_libdir}/libnvcuvid.so
%{_libdir}/nvidia/libnvidia-encode.so.%{version}
%{_libdir}/libnvidia-encode.so.1
%{_libdir}/libnvidia-encode.so
%{_libdir}/nvidia/libnvidia-opticalflow.so.%{version}
%{_libdir}/libnvidia-opticalflow.so.1
%{_libdir}/libnvidia-opticalflow.so
%{_datadir}/nvidia/nvoptix.bin

%files -n nvidia-vdpau
%defattr(-,root,root,-)
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/*
%{_libdir}/libvdpau_nvidia.so.1
%{_libdir}/libvdpau_nvidia.so

%files -n nvidia-persistenced
%defattr(-,root,root,-)
%doc nvidia-persistenced-init.tar.bz2
%{_bindir}/nvidia-persistenced
%{_mandir}/man1/nvidia-persistenced.1.gz

%files -n nvidia-powerd
%defattr(-,root,root,-)
%{_bindir}/nvidia-powerd
%{_unitdir}/nvidia-powerd.service
%{_datadir}/dbus-1/system.d/nvidia-powerd.conf

%files -n nvidia-settings
%defattr(-,root,root,-)
%{_bindir}/nvidia-settings
%{_libdir}/nvidia/libnvidia-gtk2.so.%{version}
%{_libdir}/libnvidia-gtk2.so.0
%{_libdir}/nvidia/libnvidia-gtk3.so.%{version}
%{_libdir}/libnvidia-gtk3.so.0
%{_libdir}/nvidia/libnvidia-wayland-client.so.%{version}
%{_libdir}/libnvidia-wayland-client.so.0
%{_datadir}/icons/hicolor/128x128/apps/nvidia-settings.png
%{_datadir}/applications/nvidia-settings.desktop
%{_mandir}/man1/nvidia-settings.1.gz

%files -n nvidia-X
%defattr(-,root,root,-)
%{_bindir}/nvidia-xconfig
%{_libdir}/nvidia/libnvidia-fbc.so.%{version}
%{_libdir}/libnvidia-fbc.so.1
%{_libdir}/libnvidia-fbc.so
%dir %{_libdir}/xorg
%{_libdir}/xorg/**
%{_mandir}/man1/nvidia-xconfig.1.gz

%files -n nvidia-ngx
%defattr(-,root,root,-)
%{_bindir}/nvidia-ngx-updater
%{_libdir}/nvidia/libnvidia-ngx.so.%{version}
%{_libdir}/libnvidia-ngx.so.1

%files -n nvidia-security
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-pkcs11.so.%{version}
%{_libdir}/libnvidia-pkcs11.so.1
%{_libdir}/nvidia/libnvidia-pkcs11-openssl3.so.%{version}
%{_libdir}/libnvidia-pkcs11-openssl3.so.1

%files -n nvidia-utils
%defattr(-,root,root,-)
%{_bindir}/nvidia-bug-report.sh
%{_bindir}/nvidia-debugdump
%dir %{_prefix}/lib/nvidia
%{_prefix}/lib/nvidia/*

%files -n nvidia-devel
%defattr(-,root,root,-)
%dir %{_prefix}/src/nvidia-%{version}
%{_prefix}/src/nvidia-%{version}/**

%changelog
