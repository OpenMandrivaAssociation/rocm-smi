Name:		rocm-smi
Version:	7.14.0
Release:	1
Summary:	ROCm System Management Interface Library
License:	NCSA AND MIT AND BSD
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm_smi_lib
Source0:	https://github.com/ROCm/rocm-systems/releases/download/therock-7.14/rocm-smi-lib.tar.gz#/rocm-smi-lib-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	python3

ExclusiveArch:	%{x86_64} %{aarch64}

%description
The ROCm System Management Interface Library (librocm_smi64) provides a
user-space interface for monitoring and controlling AMD GPUs.

%package devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and CMake package for the ROCm SMI library.

%prep
%autosetup -n rocm-smi-lib -p1
# Don't override distro CFLAGS
sed -i '/CMAKE_C.*_FLAGS/d' CMakeLists.txt 2>/dev/null || true

%cmake \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DBUILD_TESTS=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
# Upstream embeds a non-RPM-safe version string when not a git checkout
sed -i -e 's/= 7\.[0-9.]*.*-local-build.*/= %{version}/' \
	-e 's/PACKAGE_VERSION "[^"]*"/PACKAGE_VERSION "%{version}"/' \
	%{buildroot}%{_libdir}/cmake/rocm_smi/rocm_smi-config-version.cmake \
	%{buildroot}%{_libdir}/cmake/rocm_smi/rocm_smi-config.cmake 2>/dev/null || true

%files
%license LICENSE.md
%{_bindir}/rocm-smi
%{_libexecdir}/rocm_smi/
%{_libdir}/librocm_smi64.so.1{,.*}
%{_libdir}/liboam.so.1{,.*}
%exclude %{_docdir}/rocm-smi-lib/LICENSE.md

%files devel
%{_includedir}/rocm_smi/
%{_includedir}/oam/
%{_libdir}/librocm_smi64.so
%{_libdir}/liboam.so
%{_libdir}/cmake/rocm_smi/
