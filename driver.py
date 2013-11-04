#!/usr/bin/env python

import os, random, subprocess, glob, time

INDEX = 1

def makePcap( experiment_type ):
  global INDEX
  subprocess.Popen(['tcpdump', '-i', 'em1', '-w', experiment_type + '%d.pcap' % INDEX])
  starttime = time.time()
  subprocess.call(['./client.py'])
  endtime   = time.time()
  clienttime = open( experiment_type + '%d.pcap.time' % INDEX, 'w' )
  clienttime.write( str(endtime - starttime) )
  clienttime.close()
  INDEX += 1
  subprocess.call(['killall', 'tcpdump'])

NUM_RUNS = 30
pcaps = [ f for f in os.listdir('.') if f.endswith('.pcap') ]
csvs  = [ f for f in os.listdir('.') if f.endswith('.csv')  ]
times = [ f for f in os.listdir('.') if f.endswith('.time')  ]

for f in pcaps + csvs + times:
  os.remove(f)

experiments = [['ACK_ON__DLY_LO'] * NUM_RUNS,
               ['ACK_OFF_DLY_LO'] * NUM_RUNS,
               ['ACK_ON__DLY_HI'] * NUM_RUNS,
               ['ACK_OFF_DLY_HI'] * NUM_RUNS]

experiments = [entry for sublist in experiments for entry in sublist]
random.shuffle(experiments)

ack_on__dly_lo_file = open( 'ack_on__dly_lo.csv', 'w' )
ack_off_dly_lo_file = open( 'ack_off_dly_lo.csv', 'w' )
ack_on__dly_hi_file = open( 'ack_on__dly_hi.csv', 'w' )
ack_off_dly_hi_file = open( 'ack_off_dly_hi.csv', 'w' )

data_files = {
    'ACK_ON__DLY_LO' : ack_on__dly_lo_file,
    'ACK_OFF_DLY_LO' : ack_off_dly_lo_file,
    'ACK_ON__DLY_HI' : ack_on__dly_hi_file,
    'ACK_OFF_DLY_HI' : ack_off_dly_hi_file
}

ubuntu1actions = {
    'ACK_ON__DLY_LO' : ['ssh', 'ubuntu1', "echo 1 > /proc/sys/net/ipv4/tcp_sack"],
    'ACK_OFF_DLY_LO' : ['ssh', 'ubuntu1', "echo 0 > /proc/sys/net/ipv4/tcp_sack"],
    'ACK_ON__DLY_HI' : ['ssh', 'ubuntu1', "echo 1 > /proc/sys/net/ipv4/tcp_sack"],
    'ACK_OFF_DLY_HI' : ['ssh', 'ubuntu1', "echo 0 > /proc/sys/net/ipv4/tcp_sack"]
}

ubuntu2actions = {
    'ACK_ON__DLY_LO' : ['ssh', 'ubuntu2', "tc qdisc change dev eth2 root netem delay 5ms"],
    'ACK_OFF_DLY_LO' : ['ssh', 'ubuntu2', "tc qdisc change dev eth2 root netem delay 5ms"],
    'ACK_ON__DLY_HI' : ['ssh', 'ubuntu2', "tc qdisc change dev eth2 root netem delay 500ms"],
    'ACK_OFF_DLY_HI' : ['ssh', 'ubuntu2', "tc qdisc change dev eth2 root netem delay 500ms"]
}

for e in experiments:
  subprocess.call(ubuntu1actions[e])
  subprocess.call(ubuntu2actions[e])
  makePcap( e )

for f in data_files.values():
  f.write('Retransmit,Total,Percentage,Time\n')

for exp_type in ['ACK_ON__DLY_LO', 'ACK_OFF_DLY_LO', 'ACK_ON__DLY_HI', 'ACK_OFF_DLY_HI']:
  for pcap in glob.glob( exp_type + '*pcap' ):
    retrans    = subprocess.check_output( ('tshark -R tcp.analysis.retransmission -r ' + pcap).split() )
    total      = subprocess.check_output( ('tshark -r ' + pcap).split() )
    retransnum = len(retrans.splitlines())
    totalnum   = len(total.splitlines())
    if totalnum == 0: 
      percentage = 0
    else:
      percentage = float(retransnum) / float(totalnum)
    timefile   = open( pcap + '.time', 'r' )
    time       = ',' + timefile.readlines()[0]
    timefile.close()
    data_files[exp_type].write( str(retransnum) + ',' + str(totalnum) + ',' + str(percentage) + time + '\n' )

for f in data_files.values():
  f.close()
