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

names <- list(
   'acknowledgment: off delay: 0 +- 0'
  ,'acknowledgment: on delay: 0 +- 0'
  ,'acknowledgment: off delay: 100 +- 4'
  ,'acknowledgment: on delay: 100 +- 40'
  ,'acknowledgment: off delay: 500 +- 0'
  ,'acknowledgment: on delay: 500 +- 0'
  ,'acknowledgment: off delay: 50 +- 0'
  ,'acknowledgment: on delay: 50 +- 0'
  ,'acknowledgment: off delay: 50 +- 10'
  ,'acknowledgment: on delay: 50 +- 10'
  ,'acknowledgment: off delay: 5 +- 0'
  ,'acknowledgment: on delay: 5 +- 0'
  ,'acknowledgment: off delay: 5 +- 2'
  ,'acknowledgment: on delay: 5 +- 2'
  )

x = 1
len = length(csvs)
for ( i in 1:len ) {
  print(sprintf('============================================  Row %d =========================================================', x))
  x = x + 1
  for (j in 1:len) {
    # t-test: # independent 2-group, 2 level IV
    t <- t.test(csvs[[i]]$Retransmit, csvs[[j]]$Retransmit)
    if(t$p.value < 0.05)
    {
      print(sprintf("(%d,%d) %s, %s", i, j, names[i], names[j]))
      print(c('p-value: ', t$p.value))
      print(t$estimate)
    }
    else
    {
      print(sprintf("(%d,%d) %s, %s :::::::::::::: NO STATISTICAL SIGNIFICANCE", i, j, names[i], names[j]))
    }
  }
}


