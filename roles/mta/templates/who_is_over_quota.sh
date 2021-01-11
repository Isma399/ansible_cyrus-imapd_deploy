#!/bin/bash

mailq | grep -A1 'Over quota' | grep '@{{ mail_domain }}' |  awk -F'@' '{print $1}' | awk '{print $1}' |sort |uniq
