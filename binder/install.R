install.packages('magicaxis')
install.packages('pracma')
install.packages('cooltools')
install.packages('ellipse')
install.packages('extraDistr')

install.packages('devtools')
devtools::install_github('obreschkow/cooltools')

install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'uuid', 'digest'))

devtools::install_github('IRkernel/IRkernel')

IRkernel::installspec(user = FALSE)
