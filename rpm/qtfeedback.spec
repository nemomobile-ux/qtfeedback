Name:       qt5-qtfeedback
Summary:    Qt Feedback
Version:    5.0.2
Release:    1%{?dist}
Group:      Qt/Qt
License:    LGPLv2.1 with exception or GPLv3
URL:        http://qt.nokia.com
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
%if !0%{?fedora}
BuildRequires:  qt5-qmake
BuildRequires:  qt5-tools
%endif
BuildRequires:  fdupes

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the Qt Feedback library

%package devel
Summary:    Qt QtFeedback - development files
Group:      Qt/Qt
Requires:   %{name} = %{version}-%{release}

%description devel
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.
.
This package contains the QtFeedback module development files

%prep
%setup -q -n %{name}-%{version}

%build
touch .git # To make sure syncqt is used
%qmake5 CONFIG+=package multimedia_disabled=yes
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%qmake5_install

# Fix wrong path in pkgconfig files
find %{buildroot}%{_libdir}/pkgconfig -type f -name '*.pc' \
-exec perl -pi -e "s, -L%{_builddir}/?\S+,,g" {} \;
# Fix wrong path in prl files
find %{buildroot}%{_libdir} -type f -name '*.prl' \
-exec sed -i -e "/^QMAKE_PRL_BUILD_DIR/d;s/\(QMAKE_PRL_LIBS =\).*/\1/" {} \;
# Remove unneeded .la files
rm -f %{buildroot}/%{_libdir}/*.la

# We don't need qt5/Qt/
rm -rf %{buildroot}/%{_includedir}/qt5/Qt

# Replace the old Qt0Feedback.pc with Qt5Feedback.pc
cp %{buildroot}/%{_libdir}/pkgconfig/Qt5Feedback.pc %{buildroot}/%{_libdir}/pkgconfig/Qt0Feedback.pc

%fdupes %{buildroot}/%{_includedir}


%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libQt5Feedback.so.0
%{_libdir}/libQt5Feedback.so.0.*
%{_libdir}/qt5/qml/

%files devel
%defattr(-,root,root,-)
%{_libdir}/libQt5Feedback.so
%{_libdir}/libQt5Feedback.prl
%{_libdir}/pkgconfig/*
%{_includedir}/qt5/*
%{_prefix}/*/qt5/mkspecs/
%{_libdir}/cmake/
