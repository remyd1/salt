# -*- coding: utf-8 -*-
'''
Disk monitoring state

Monitor the state of disk resources

Check blkid and test disk type

.. code-block:: yaml
  
  disk_status:
    disk.status:
      - name: /media/sda1
      - maximum: 95%
      - minimum: 5%

  disk_blkid:
    disk.blkid:
        - name: /dev/sda1
        - disktype: zfs

'''
from __future__ import absolute_import

# Import salt libs
from salt.ext.six import string_types

__monitor__ = [
        'status',
        ]

def blkid(name, disktype):
    '''
    Return the blkid informations like disk.blkid
    No changes will be made

    '''
    ret = {'name': name,
           'result': False,
           'comment': '',
           'raw_value' : '',
           'type': '',
           'changes': {}}

    data = __salt__['disk.blkid']()
    if name not in data:
        ret['result'] = False
        ret['comment'] = 'Named disk not present: {0}'.format(name)
        return ret
    else:
        ret['result'] = True
        if disktype:
            if disktype in data[name]['TYPE']:
                ret['type'] = data[name]['TYPE']
                data[name]['comment'] = 'Your {0} type has been found !'.format(disktype)
                ret['comment'] = data[name]
            else:
                ret['result'] = False
                ret['comment'] = 'Your {0} type has not been found !'.format(disktype)
        return ret



def status(name, maximum=None, minimum=None):
    '''
    Return the current disk usage stats for the named mount point
    '''
    # Monitoring state, no changes will be made so no test interface needed
    ret = {'name': name,
           'result': False,
           'comment': '',
           'changes': {},
           'data': {}}  # Data field for monitoring state

    data = __salt__['disk.usage']()
    if name not in data:
        ret['result'] = False
        ret['comment'] += 'Named disk mount not present '
        return ret
    if maximum:
        try:
            if isinstance(maximum, string_types):
                maximum = int(maximum.strip('%'))
        except Exception:
            ret['comment'] += 'Max argument must be an integer '
    if minimum:
        try:
            if isinstance(minimum, string_types):
                minimum = int(minimum.strip('%'))
        except Exception:
            ret['comment'] += 'Min argument must be an integer '
    if minimum and maximum:
        if minimum >= maximum:
            ret['comment'] += 'Min must be less than max'
    if ret['comment']:
        return ret
    cap = int(data[name]['capacity'].strip('%'))
    ret['data'] = data[name]
    if minimum:
        if cap < minimum:
            ret['comment'] = 'Disk is below minimum of {0}% at {1}'.format(
                    minimum, cap)
            return ret
    if maximum:
        if cap > maximum:
            ret['comment'] = 'Disk is above maximum of {0}% at {1}'.format(
                    maximum, cap)
            return ret
    ret['comment'] = 'Disk in acceptable range'
    ret['result'] = True
    return ret
