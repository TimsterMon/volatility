
import sys
import volatility.debug as debug
import volatility.obj as obj

# SSDT structures for all x86 profiles *except* Win 2003 Server
ssdt_vtypes = {
    '_SERVICE_DESCRIPTOR_TABLE' : [ 0x40, {
    'Descriptors' : [0x0, ['array', 4, ['_SERVICE_DESCRIPTOR_ENTRY']]],
    }],
    '_SERVICE_DESCRIPTOR_ENTRY' : [ 0x10, {
    'KiServiceTable' : [0x0, ['pointer', ['void']]],
    'CounterBaseTable' : [0x4, ['pointer', ['unsigned long']]],
    'ServiceLimit' : [0x8, ['unsigned long']],
    'ArgumentTable' : [0xc, ['pointer', ['unsigned char']]],
    }],
}

# SSDT structures for Win 2003 Server x86
ssdt_vtypes_2k3 = {
    '_SERVICE_DESCRIPTOR_TABLE' : [ 0x20, {
    'Descriptors' : [0x0, ['array', 2, ['_SERVICE_DESCRIPTOR_ENTRY']]],
    }],
}

# SSDT structures for x64
ssdt_vtypes_64 = {
    '_SERVICE_DESCRIPTOR_TABLE' : [ 0x40, {
    'Descriptors' : [0x0, ['array', 2, ['_SERVICE_DESCRIPTOR_ENTRY']]],
    }],
    '_SERVICE_DESCRIPTOR_ENTRY' : [ 0x20, {
    'KiServiceTable' : [0x0, ['pointer64', ['void']]],
    'CounterBaseTable' : [0x8, ['pointer64', ['unsigned long']]],
    'ServiceLimit' : [0x10, ['unsigned long long']],
    'ArgumentTable' : [0x18, ['pointer64', ['unsigned char']]],
    }],
}

#### Filthy Hack for backwards compatibility

def syscalls_property(x):
    debug.debug("Deprecation warning: Please use profile.additional['syscalls'] over profile.syscalls")
    return x.additional.get('syscalls', [[], []])

class WinSyscallsAttribute(obj.Hook):
    conditions = {'os': lambda x: x == 'windows'}

    def modification(self, profile):
        # Filthy hack for backwards compatibilitiy
        profile.__class__.syscalls = property(syscalls_property)

####

class AbstractSyscalls(obj.Hook):
    syscall_module = 'No default'
    def modification(self, profile):
        module = sys.modules.get(self.syscall_module, None)
        profile.additional['syscalls'] = module.syscalls

class WinXPSyscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.xp_sp2_x86_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '32bit',
                  'major': lambda x : x == 5,
                  'minor': lambda x : x == 1}

class WinXPx64Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.win2k3_sp12_x64_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '64bit',
                  'major': lambda x : x == 5,
                  'minor': lambda x : x == 2}

class Win2K3SP0Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.win2k3_sp0_x86_syscalls'
    before = ['Win2K3SP12Syscalls']
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '32bit',
                  'major': lambda x: x == 5,
                  'minor': lambda x: x == 2,
                  'build': lambda x: x == 3789}

class Win2K3SP12Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.win2k3_sp12_x86_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '32bit',
                  'major': lambda x : x == 5,
                  'minor': lambda x : x == 2}

class VistaSP0Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.vista_sp0_x86_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '32bit',
                  'major': lambda x : x == 6,
                  'minor': lambda x : x == 0,
                  'build': lambda x : x == 6000}

class VistaSP0x64Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.vista_sp0_x64_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '64bit',
                  'major': lambda x : x == 6,
                  'minor': lambda x : x == 0,
                  'build': lambda x : x == 6000}

class VistaSP12Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.vista_sp12_x86_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '32bit',
                  'major': lambda x : x == 6,
                  'minor': lambda x : x == 0,
                  'build': lambda x : x >= 6001}

class VistaSP12x64Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.vista_sp12_x64_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '64bit',
                  'major': lambda x : x == 6,
                  'minor': lambda x : x == 0,
                  'build': lambda x : x >= 6001}

class Win7SP01Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.win7_sp01_x86_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '32bit',
                  'major': lambda x : x == 6,
                  'minor': lambda x : x == 1}

class Win7SP01x64Syscalls(AbstractSyscalls):
    syscall_module = 'volatility.plugins.overlays.windows.win7_sp01_x64_syscalls'
    conditions = {'os': lambda x: x == 'windows',
                  'memory_model': lambda x: x == '64bit',
                  'major': lambda x : x == 6,
                  'minor': lambda x : x == 1}
