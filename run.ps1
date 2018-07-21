Param(
[Parameter(Mandatory=$True,Position=1)]
[string]$date
)

$dates = @("2017-07-01","2017-08-01","2017-09-01","2017-10-01","2017-11-01","2017-12-01","2018-01-01","2018-02-01","2018-03-01","2018-04-01","2018-05-01","2018-06-01","2018-07-01")

foreach ($date in $dates){
  #py combine_data_lim.py $date
  py tsf_var.py $date $date
}


# Rscript -e "rmarkdown::render('TSF_Risk_Monthly.rmd')" --args 2018-07-01
