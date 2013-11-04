setwd('~/Dropbox/CS585/Lab1/data/lab1/csvs/')

off_d0v0    = read.csv( '0v0__ack_off_dly_lo.csv'    )
on__d0v0    = read.csv( '0v0__ack_on__dly_lo.csv'    )
off_d100v4  = read.csv( '100v40__ack_off_dly_hi.csv' )
on__d100v40 = read.csv( '100v40__ack_on__dly_hi.csv' )
off_d500v0  = read.csv( '500v0__ack_off_dly_hi.csv'  )
on__d500v0  = read.csv( '500v0__ack_on__dly_hi.csv'  )
off_d50v0   = read.csv( '50v0__ack_off_dly_hi.csv'   )
on__d50v0   = read.csv( '50v0__ack_on__dly_hi.csv'   )
off_d50v10  = read.csv( '50v10__ack_off_dly_hi.csv'  )
on__d50v10  = read.csv( '50v10__ack_on__dly_hi.csv'  )
off_d5v0    = read.csv( '5v0__ack_off_dly_lo.csv'    )
on__d5v0    = read.csv( '5v0__ack_on__dly_lo.csv'    )
off_d5v2    = read.csv( '5v2__ack_off_dly_lo.csv'    )
on__d5v2    = read.csv( '5v2__ack_on__dly_lo.csv'    )

csvs <- list(
   off_d0v0
  ,on__d0v0
  ,off_d100v4
  ,on__d100v40
  ,off_d500v0
  ,on__d500v0
  ,off_d50v0
  ,on__d50v0
  ,off_d50v10
  ,on__d50v10
  ,off_d5v0
  ,on__d5v0
  ,off_d5v2
  ,on__d5v2
)

x = 1
for (i in csvs) {
  print(sprintf('============================================  Row %d =========================================================', x))
  x = x + 1
  for (j in csvs) {
    # t-test: # independent 2-group, 2 level IV
    t <- t.test(i$Retransmit, j$Retransmit)
    if(t$p.value < 0.05)
    {
      print(c('p-value: ', t$p.value))
      print(t$estimate)
    }
    else
    {
      print("N/A")
    }
  }
}

