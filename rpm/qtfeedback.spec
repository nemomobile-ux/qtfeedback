Name:       qt5-qtfeedback
Summary:    Qt Feedback
Version:    5.0.2
Release:    1%{?dist}
Group:      Qt/Qt
License:    LGPLv2.1 with exception or GPLv3
URL:        http://qt.nokia.com
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  qt5-qtcore-devel
BuildRequires:  qt5-qtgui-devel
BuildRequires:  qt5-qtopengl-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtdeclarative-qtquick-devel
BuildRequires:  qt5-qmake
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


#### Build section

%prep
%setup -q -n %{name}-%{version}/qtfeedback

%build
export QTDIR=/usr/share/qt5
touch .git # To make sure syncqt is used

%qmake5 CONFIG+=package VERSION=`echo %{version} | sed 's/+.*//'`
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


%fdupes %{buildroot}/%{_includedir}


#### Pre/Post section

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

#### File section
%files
%defattr(-,root,root,-)
%{_libdir}/libQt5Feedback.so*
%{_libdir}/qt5/qml/

%files devel
%defattr(-,root,root,-)
%{_libdir}/libQt5Feedback.prl
%{_libdir}/pkgconfig/*
%{_includedir}/qt5/*
%{_datadir}/qt5/mkspecs/
%{_libdir}/cmake/
