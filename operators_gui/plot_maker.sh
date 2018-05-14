#!/usr/bin/env bash

gnuplot << EOP

datafile = "plot_data_counts.txt"

set terminal png font arial 10 size 1250,205


set output "plot_count.png"
set grid x y
set xtics 1
#set xlabel "Часы смены"
#set ylabel "Рейсы"

plot datafile using 1:2 title "Статистика по рейсам" with lines lt rgb "red" lw 2

EOP

gnuplot << EOP

datafile = "plot_data_counts.txt"

set terminal png font arial 10 size 1250,205
set output "plot_sum.png"
set grid x y
#set xlabel "Часы смены"
#set ylabel "Тонны"
set xtics 1

plot datafile using 1:3 title "Статистика по массе" with lines lt rgb "green" lw 2
EOP