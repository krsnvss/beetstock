#!/usr/bin/env bash

gnuplot << EOP

datafile = "./operators_gui/plot_data.txt"

set terminal png font arial 8 size 1250,205

set output "./res/plot_count.png"
set grid x y

set xdata time
set timefmt "%d.%m/%H:%M"
set format x "%d.%m/%H:%M"

#set xtics 1
#set xlabel "Часы смены"
#set ylabel "Рейсы"

plot datafile using 1:2 title "Статистика по рейсам" with lines lt rgb "red" lw 2

EOP

gnuplot << EOP

datafile = "./operators_gui/plot_data.txt"

set terminal png font arial 8 size 1250,205

set output "./res/plot_sum.png"
set grid x y

set xdata time
set timefmt "%d.%m/%H:%M"
set format x "%d.%m/%H:%M"

#set xtics 1
#set xlabel "Часы смены"
#set ylabel "Тонны"

plot datafile using 1:3 title "Статистика по тоннам" with lines lt rgb "green" lw 2

EOP