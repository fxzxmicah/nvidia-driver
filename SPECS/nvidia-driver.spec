%define kernel_rel %(dnf repoquery kernel-devel --latest-limit=1 --queryformat="%%{VERSION}-%%{RELEASE}")
%define kernel_ver %(dnf repoquery kernel-devel --latest-limit=1 --queryformat="%%{VERSION}")

%define sign_tool %(base64 -w 0 %{_prefix}/src/kernels/%{kernel_rel}.%{_arch}/scripts/sign-file)

%if 0%{?__isa_bits} == 64
%global elf_bits (64bit)
%endif

Name:                   nvidia-driver
Version:                550.144.03
Release:                1%{?dist}
Summary:                NVIDIA binary driver for Linux
License:                NVIDIA
URL:                    http://www.nvidia.com/
Source0:                https://download.nvidia.com/XFree86/Linux-%{_arch}/%{version}/NVIDIA-Linux-%{_arch}-%{version}-no-compat32.run
Source1:                https://download.nvidia.com/XFree86/Linux-%{_arch}/%{version}/NVIDIA-Linux-%{_arch}-%{version}-no-compat32.run.sha256sum

Source2:                nouveau.conf
Source3:                nvidia.conf
Source4:                86-nvidia-driver.preset

BuildRequires:          gcc
BuildRequires:          make
BuildRequires:          kernel-devel
BuildRequires:          systemd-rpm-macros
BuildRequires:          jq

Requires:               nvidia-modules%{?_isa} = %{version}-%{release}

Requires:               systemd

ExclusiveArch:          x86_64

%description
The NVIDIA Linux graphics driver.

%package -n nvidia-gpu-firmware
Summary:                NVIDIA Graphics firmware
Group:                  System Environment/Hardware

%description -n nvidia-gpu-firmware
NVIDIA Graphics firmware

%package -n nvidia-common
Summary:                NVIDIA Graphics common files
Group:                  System Environment/Kernel

Requires:               nvidia-modules%{?_isa} = %{version}-%{release}

Requires:               module-init-tools

%%description -n nvidia-common
NVIDIA Graphics common files

%package -n nvidia-modules-%{kernel_ver}
Summary:                NVIDIA Graphics kernel modules
Group:                  System Environment/Kernel

Requires:               kernel%{?_isa} = %{kernel_rel}
Requires:               kernel-core%{?_isa} = %{kernel_rel}

Requires:               nvidia-gpu-firmware%{?_isa} = %{version}-%{release}
Requires:               nvidia-common%{?_isa} = %{version}-%{release}

Requires(post):         %{_bindir}/base64
Requires(post):         libcrypto.so.3()%{?elf_bits}
Requires(post):         libc.so.6()%{?elf_bits}
Requires(post):         libz.so.1()%{?elf_bits}
Requires(post):         ld-linux-x86-64.so.2()%{?elf_bits}

Requires(posttrans):    %{_bindir}/kernel-install

Provides:               nvidia-modules%{?_isa} = %{version}-%{release}

%description -n nvidia-modules-%{kernel_ver}
NVIDIA graphics kernel modules (Closed Source Version)

%package -n nvidia-egl
Summary:                NVIDIA EGL libraries

Requires:               %{name}%{?_isa} = %{version}-%{release}

Requires(post):         alternatives
Requires(preun):        alternatives

%description -n nvidia-egl
NVIDIA EGL libraries

%package -n nvidia-wayland
Summary:                NVIDIA Wayland libraries

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-wayland
NVIDIA Wayland libraries

%package -n nvidia-gbm
Summary:                NVIDIA GBM libraries

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-gbm
NVIDIA GBM libraries

%package -n nvidia-opencl
Summary:                NVIDIA OpenCL libraries

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-opencl
NVIDIA OpenCL libraries

%package -n nvidia-cuda
Summary:                NVIDIA CUDA libraries

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-cuda
NVIDIA CUDA libraries

%package -n nvidia-vision
Summary:                NVIDIA Vision libraries

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-vision
NVIDIA Vision libraries

%package -n nvidia-vdpau
Summary:                NVIDIA VDPAU libraries

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-vdpau
NVIDIA VDPAU libraries

%package -n nvidia-persistenced
Summary:                NVIDIA Persistenced Utilities

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-persistenced
NVIDIA Persistenced Utilities

%package -n nvidia-powerd
Summary:                NVIDIA Powerd Utilities

Requires:               %{name}%{?_isa} = %{version}-%{release}

Requires:               dbus
Requires:               systemd

%description -n nvidia-powerd
NVIDIA Powerd Utilities

%package -n nvidia-settings
Summary:                NVIDIA Settings Application

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-settings
NVIDIA Settings Application

%package -n nvidia-X
Summary:                NVIDIA X drivers

Requires:               %{name}%{?_isa} = %{version}-%{release}

Requires:               xorg-x11-server-Xorg

Requires(post):         alternatives
Requires(preun):        alternatives

%description -n nvidia-X
NVIDIA X drivers

%package -n nvidia-ngx
Summary:                NVIDIA NGX Utilities

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-ngx
NVIDIA NGX Utilities

%package -n nvidia-security
Summary:                NVIDIA Security Libraries

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-security
NVIDIA Security Libraries

%package -n nvidia-utils
Summary:                NVIDIA Utilities

Requires:               %{name}%{?_isa} = %{version}-%{release}

%description -n nvidia-utils
NVIDIA Utilities

%package -n nvidia-devel
Summary:                NVIDIA Development Files

%description -n nvidia-devel
NVIDIA Development Files

%prep
cd %{_sourcedir}
# Verify sha256sum
sha256sum -c %{SOURCE1}

rm -r %{_builddir}
sh %{SOURCE0} --extract-only --target %{_builddir}

%build
cd %{_builddir}/kernel
export SYSSRC=%{_prefix}/src/kernels/%{kernel_rel}.%{_arch}
export SYSOUT=$SYSSRC
export NV_EXCLUDE_KERNEL_MODULES="nvidia-vgpu-vfio nvidia-peermem"
%{make_build} modules

# Strip modules
strip --strip-unneeded *.ko

%install
mkdir -p %{buildroot}/lib/firmware/nvidia/%{version}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}-sleep
mkdir -p %{buildroot}%{_prefix}/lib/nvidia
mkdir -p %{buildroot}%{_libdir}/nvidia
mkdir -p %{buildroot}%{_libdir}/gbm
mkdir -p %{buildroot}%{_sysconfdir}/OpenCL/vendors
mkdir -p %{buildroot}%{_datadir}/dbus-1/system.d
mkdir -p %{buildroot}%{_datadir}/nvidia
mkdir -p %{buildroot}%{_datadir}/nvidia/vulkan
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_libdir}/xorg/modules/extensions
mkdir -p %{buildroot}%{_datadir}/X11/xorg.conf.d
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d
mkdir -p %{buildroot}%{_libdir}/xorg/modules/drivers
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}%{_libdir}/vdpau
mkdir -p %{buildroot}/lib/modules/%{kernel_rel}.%{_arch}/kernel/drivers/video
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_prefix}/src/nvidia-%{version}

install -Dm0400 /dev/null -t %{buildroot}%{_sysconfdir}/keys/modsign.key
install -Dm0444 /dev/null -t %{buildroot}%{_sysconfdir}/keys/modsign.der
install -Dm0644 /dev/null -t %{buildroot}%{_datadir}/vulkan/icd.d/nvidia_icd.json
install -Dm0644 /dev/null -t %{buildroot}%{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json

mv firmware/* %{buildroot}/lib/firmware/nvidia/%{version}
mv nvidia-bug-report.sh %{buildroot}%{_bindir}
mv nvidia-modprobe %{buildroot}%{_bindir}
mv nvidia-modprobe.1.gz %{buildroot}%{_mandir}/man1
mv systemd/system/* %{buildroot}%{_unitdir}
mv systemd/system-sleep/* %{buildroot}%{_unitdir}-sleep
mv systemd/nvidia-sleep.sh %{buildroot}%{_bindir}
mv libglvnd_install_checker/* %{buildroot}%{_prefix}/lib/nvidia
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
mv nvidia_icd.json %{buildroot}%{_datadir}/nvidia/vulkan
mv nvidia_layers.json %{buildroot}%{_datadir}/nvidia/vulkan
mv nvidia-application-profiles-%{version}-* %{buildroot}%{_datadir}/nvidia
mv libGLX_nvidia.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-glsi.so.%{version} %{buildroot}%{_libdir}/nvidia
mv libnvidia-glvkspirv.so.%{version} %{buildroot}%{_libdir}/nvidia
mv 10_nvidia.json %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mv libglxserver_nvidia.so.%{version} %{buildroot}%{_libdir}/xorg/modules/extensions
mv nvidia-drm-outputclass.conf %{buildroot}%{_datadir}/X11/xorg.conf.d
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
mv kernel/*.ko %{buildroot}/lib/modules/%{kernel_rel}.%{_arch}/kernel/drivers/video
mv nvidia-settings.desktop %{buildroot}%{_datadir}/applications
mv kernel/* %{buildroot}%{_prefix}/src/nvidia-%{version}

install -Dm0644 %{SOURCE2} -t %{buildroot}%{_prefix}/lib/modprobe.d
install -Dm0644 %{SOURCE3} -t %{buildroot}%{_prefix}/lib/modprobe.d
install -Dm0644 %{SOURCE4} -t %{buildroot}%{_unitdir}-preset

jq .ICD.library_path=\"libEGL_nvidia.so.0\" %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_icd.json > %{buildroot}%{_datadir}/nvidia/vulkan/egl-nvidia_icd.json
jq .layers[0].library_path=\"libEGL_nvidia.so.0\" %{buildroot}%{_datadir}/nvidia/vulkan/nvidia_layers.json > %{buildroot}%{_datadir}/nvidia/vulkan/egl-nvidia_layers.json

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
ln -sr nvidia/libnvidia-gpucomp.so.%{version} libnvidia-gpucomp.so.%{version}
ln -sr nvidia/libnvidia-api.so.* libnvidia-api.so.1
ln -sr nvidia/libnvidia-glcore.so.%{version} libnvidia-glcore.so.%{version}
ln -sr nvidia/libnvidia-tls.so.%{version} libnvidia-tls.so.%{version}
ln -sr nvidia/libGLX_nvidia.so.%{version} libGLX_nvidia.so.0
ln -sr nvidia/libnvidia-glsi.so.%{version} libnvidia-glsi.so.%{version}
ln -sr nvidia/libnvidia-glvkspirv.so.%{version} libnvidia-glvkspirv.so.%{version}
ln -sr xorg/modules/extensions/libglxserver_nvidia.so.%{version} xorg/modules/extensions/libglxserver_nvidia.so
ln -sr nvidia/libnvidia-eglcore.so.%{version} libnvidia-eglcore.so.%{version}
ln -sr nvidia/libEGL_nvidia.so.%{version} libEGL_nvidia.so.0
ln -sr nvidia/libGLESv2_nvidia.so.%{version} libGLESv2_nvidia.so.2
ln -sr nvidia/libGLESv1_CM_nvidia.so.%{version} libGLESv1_CM_nvidia.so.1
ln -sr nvidia/libnvidia-egl-wayland.so.* libnvidia-egl-wayland.so.1
ln -sr nvidia/libnvidia-egl-gbm.so.* libnvidia-egl-gbm.so.1
ln -sr nvidia/libnvidia-gtk2.so.%{version} libnvidia-gtk2.so.%{version}
ln -sr nvidia/libnvidia-gtk3.so.%{version} libnvidia-gtk3.so.%{version}
ln -sr nvidia/libnvidia-wayland-client.so.%{version} libnvidia-wayland-client.so.%{version}
ln -sr nvidia/libnvidia-cfg.so.%{version} libnvidia-cfg.so.1
ln -sr vdpau/libvdpau_nvidia.so.%{version} vdpau/libvdpau_nvidia.so.1
ln -sr vdpau/libvdpau_nvidia.so.1 libvdpau_nvidia.so
ln -sr nvidia/libnvidia-allocator.so.%{version} libnvidia-allocator.so.1
ln -sr libnvidia-allocator.so.1 gbm/nvidia-drm_gbm.so
ln -sr libnvidia-allocator.so.1 libnvidia-allocator.so
ln -sr nvidia/libnvidia-rtcore.so.%{version} libnvidia-rtcore.so.%{version}
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
ln -sr nvidia/libnvidia-pkcs11.so.%{version} libnvidia-pkcs11.so.%{version}
ln -sr nvidia/libnvidia-pkcs11-openssl3.so.%{version} libnvidia-pkcs11-openssl3.so.%{version}

cd %{buildroot}%{_prefix}/src/nvidia-%{version}
ln -srf nvidia-modeset/nv-modeset-kernel.o_binary nvidia-modeset/nv-modeset-kernel.o
ln -srf nvidia/nv-kernel.o_binary nvidia/nv-kernel.o

%check
ls -l * > %{_topdir}/leaves.list

%post
%systemd_post nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service

%post -n nvidia-modules-%{kernel_ver}
if [ -f %{_sysconfdir}/keys/modsign.key ] && [ -f %{_sysconfdir}/keys/modsign.der ]; then
    chown root:root %{_sysconfdir}/keys/modsign.*
    chmod 400 %{_sysconfdir}/keys/modsign.key
    chmod 444 %{_sysconfdir}/keys/modsign.der
    echo %{sign_tool} | base64 -d > %{_tmppath}/sign-file
    chmod +x %{_tmppath}/sign-file
    for module in /lib/modules/%{kernel_rel}.%{_arch}/kernel/drivers/video/*.ko; do
        %{_tmppath}/sign-file sha256 %{_sysconfdir}/keys/modsign.key %{_sysconfdir}/keys/modsign.der $module
    done
    rm -f %{_tmppath}/sign-file
fi
/sbin/depmod -a %{kernel_rel}.%{_arch}

%post -n nvidia-egl
update-alternatives --install %{_datadir}/vulkan/icd.d/nvidia_icd.json nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/egl-nvidia_icd.json 25 --follower %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json nvidia-vulkan-layers %{_datadir}/nvidia/vulkan/egl-nvidia_layers.json

%post -n nvidia-powerd
%systemd_post nvidia-powerd.service

%post -n nvidia-X
update-alternatives --install %{_datadir}/vulkan/icd.d/nvidia_icd.json nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/nvidia_icd.json 50 --follower %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json nvidia-vulkan-layers %{_datadir}/nvidia/vulkan/nvidia_layers.json

%posttrans -n nvidia-modules-%{kernel_ver}
kernel-install add %{kernel_rel}.%{_arch} /lib/modules/%{kernel_rel}.%{_arch}/vmlinuz*

%preun
%systemd_preun nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service

%preun -n nvidia-egl
if [ $1 -eq 0 ]; then
    update-alternatives --remove nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/egl-nvidia_icd.json || :
fi

%preun -n nvidia-powerd
%systemd_preun nvidia-powerd.service

%preun -n nvidia-X
if [ $1 -eq 0 ]; then
    update-alternatives --remove nvidia-vulkan-icd %{_datadir}/nvidia/vulkan/nvidia_icd.json || :
fi

%postun
%systemd_postun nvidia-suspend.service nvidia-hibernate.service nvidia-resume.service

%postun -n nvidia-modules-%{kernel_ver}
/sbin/depmod -a %{kernel_rel}.%{_arch}

%postun -n nvidia-powerd
%systemd_postun nvidia-powerd.service

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.txt
%doc NVIDIA_Changelog
%doc html
%doc supported-gpus
%attr(4755,root,root) %{_bindir}/nvidia-modprobe
%{_bindir}/nvidia-sleep.sh
%attr(4755,root,root) %{_bindir}/nvidia-smi
%dir %{_libdir}/nvidia
%{_libdir}/nvidia/libnvidia-ml.so.%{version}
%{_libdir}/libnvidia-ml.so.1
%{_libdir}/libnvidia-ml.so
%{_libdir}/nvidia/libnvidia-gpucomp.so.%{version}
%{_libdir}/libnvidia-gpucomp.so.%{version}
%{_libdir}/nvidia/libnvidia-api.so.*
%{_libdir}/libnvidia-api.so.1
%{_libdir}/nvidia/libnvidia-glcore.so.%{version}
%{_libdir}/libnvidia-glcore.so.%{version}
%{_libdir}/nvidia/libnvidia-tls.so.%{version}
%{_libdir}/libnvidia-tls.so.%{version}
%{_libdir}/nvidia/libnvidia-glsi.so.%{version}
%{_libdir}/libnvidia-glsi.so.%{version}
%{_libdir}/nvidia/libnvidia-glvkspirv.so.%{version}
%{_libdir}/libnvidia-glvkspirv.so.%{version}
%{_libdir}/nvidia/libGLESv2_nvidia.so.%{version}
%{_libdir}/libGLESv2_nvidia.so.2
%{_libdir}/nvidia/libGLESv1_CM_nvidia.so.%{version}
%{_libdir}/libGLESv1_CM_nvidia.so.1
%{_libdir}/nvidia/libnvidia-allocator.so.%{version}
%{_libdir}/libnvidia-allocator.so.1
%{_libdir}/libnvidia-allocator.so
%{_unitdir}/nvidia-suspend.service
%{_unitdir}/nvidia-hibernate.service
%{_unitdir}/nvidia-resume.service
%{_unitdir}-sleep/*
%{_unitdir}-preset/*
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-*
%{_mandir}/man1/nvidia-modprobe.1.gz
%{_mandir}/man1/nvidia-smi.1.gz

%files -n nvidia-gpu-firmware
%defattr(-,root,root,-)
%license LICENSE
%dir /lib/firmware/nvidia
%dir /lib/firmware/nvidia/%{version}
/lib/firmware/nvidia/%{version}/*

%files -n nvidia-common
%config %{_prefix}/lib/modprobe.d/*
%dir %ghost %{_sysconfdir}/keys
%config(noreplace) %ghost %{_sysconfdir}/keys/*

%files -n nvidia-modules-%{kernel_ver}
%defattr(-,root,root,-)
%license LICENSE
/lib/modules/%{kernel_rel}.%{_arch}/kernel/drivers/video/*

%files -n nvidia-egl
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-eglcore.so.%{version}
%{_libdir}/libnvidia-eglcore.so.%{version}
%{_libdir}/nvidia/libEGL_nvidia.so.%{version}
%{_libdir}/libEGL_nvidia.so.0
%ghost %{_datadir}/vulkan/icd.d/nvidia_icd.json
%ghost %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json
%{_datadir}/glvnd/egl_vendor.d/*
%{_datadir}/nvidia/vulkan/egl-nvidia_icd.json
%{_datadir}/nvidia/vulkan/egl-nvidia_layers.json

%files -n nvidia-wayland
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-egl-wayland.so.*
%{_libdir}/libnvidia-egl-wayland.so.1
%{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json

%files -n nvidia-gbm
%defattr(-,root,root,-)
%dir %{_libdir}/gbm
%{_libdir}/gbm/*
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
%config %{_sysconfdir}/OpenCL/vendors/nvidia.icd

%files -n nvidia-cuda
%defattr(-,root,root,-)
%attr(4755,root,root) %{_bindir}/nvidia-cuda-mps-control
%attr(4755,root,root) %{_bindir}/nvidia-cuda-mps-server
%{_libdir}/nvidia/libcuda.so.%{version}
%{_libdir}/libcuda.so.1
%{_libdir}/libcuda.so
%{_libdir}/nvidia/libnvidia-ptxjitcompiler.so.%{version}
%{_libdir}/libnvidia-ptxjitcompiler.so.1
%{_libdir}/libnvidia-ptxjitcompiler.so
%{_libdir}/nvidia/libcudadebugger.so.%{version}
%{_libdir}/libcudadebugger.so.1
%{_libdir}/nvidia/libnvidia-nvvm.so.%{version}
%{_libdir}/libnvidia-nvvm.so.4
%{_libdir}/libnvidia-nvvm.so
%{_mandir}/man1/nvidia-cuda-mps-control.1.gz

%files -n nvidia-vision
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-rtcore.so.%{version}
%{_libdir}/libnvidia-rtcore.so.%{version}
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
%{_libdir}/libvdpau_nvidia.so

%files -n nvidia-persistenced
%defattr(-,root,root,-)
%doc nvidia-persistenced-init.tar.bz2
%{_libdir}/nvidia/libnvidia-cfg.so.%{version}
%{_libdir}/libnvidia-cfg.so.1
%{_bindir}/nvidia-persistenced
%{_mandir}/man1/nvidia-persistenced.1.gz

%files -n nvidia-powerd
%defattr(-,root,root,-)
%{_bindir}/nvidia-powerd
%{_unitdir}/nvidia-powerd.service
%{_datadir}/dbus-1/system.d/*

%files -n nvidia-settings
%defattr(-,root,root,-)
%{_bindir}/nvidia-settings
%{_libdir}/nvidia/libnvidia-gtk2.so.%{version}
%{_libdir}/libnvidia-gtk2.so.%{version}
%{_libdir}/nvidia/libnvidia-gtk3.so.%{version}
%{_libdir}/libnvidia-gtk3.so.%{version}
%{_libdir}/nvidia/libnvidia-wayland-client.so.%{version}
%{_libdir}/libnvidia-wayland-client.so.%{version}
%{_datadir}/icons/hicolor/**
%{_datadir}/applications/*
%{_mandir}/man1/nvidia-settings.1.gz

%files -n nvidia-X
%defattr(-,root,root,-)
%attr(4755,root,root) %{_bindir}/nvidia-xconfig
%{_libdir}/nvidia/libGLX_nvidia.so.%{version}
%{_libdir}/libGLX_nvidia.so.0
%{_libdir}/nvidia/libnvidia-fbc.so.%{version}
%{_libdir}/libnvidia-fbc.so.1
%{_libdir}/libnvidia-fbc.so
%{_libdir}/xorg/**
%ghost %{_datadir}/vulkan/icd.d/nvidia_icd.json
%ghost %{_datadir}/vulkan/implicit_layer.d/nvidia_layers.json
%{_datadir}/X11/xorg.conf.d/*
%{_datadir}/nvidia/vulkan/nvidia_icd.json
%{_datadir}/nvidia/vulkan/nvidia_layers.json
%{_mandir}/man1/nvidia-xconfig.1.gz

%files -n nvidia-ngx
%defattr(-,root,root,-)
%{_bindir}/nvidia-ngx-updater
%{_libdir}/nvidia/libnvidia-ngx.so.%{version}
%{_libdir}/libnvidia-ngx.so.1

%files -n nvidia-security
%defattr(-,root,root,-)
%{_libdir}/nvidia/libnvidia-pkcs11.so.%{version}
%{_libdir}/libnvidia-pkcs11.so.%{version}
%{_libdir}/nvidia/libnvidia-pkcs11-openssl3.so.%{version}
%{_libdir}/libnvidia-pkcs11-openssl3.so.%{version}

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
