#!/bin/bash
#set -x

#we executed 10 runs of evosuite and used the average coverage
run_number=1

#root directory for input and output
main_dir="~/"

#A csv containing ckjm features for classes. We generated test suite for classes having cyclomatic complexity greater than 3. 
INPUT="${main_dir}/SF110-ckjmfeatures-spartan/ckjm-features.csv"

#evosuite in these experiments
testing_tool=""

#Directory having SF110 or Collections results
experiment_directory="SF110"

project_path="${main_dir}/${experiment_directory}"

#Test generation Algorithm
evosuite_algo="DYNAMOSA"

#Path for MAJOR mutation testing framework
major_bin="/home/unimelb.edu.au/nneelofar/Downloads/major-1.3.4_jre7/major/bin"

#path for sub-scripts used by the current script
SF110_scripts_path=""

#path for evosuite
evosuite_path="/home/unimelb.edu.au/nneelofar/Downloads/evosuite-1.1.0"

mkdir ${main_dir}/SF110-results/${evosuite_algo}
mkdir ${main_dir}/SF110-results/${evosuite_algo}/${run_number}
results_directory="${main_dir}/SF110-results-failed/${evosuite_algo}/${run_number}"
mml_path="${main_dir}"
mkdir -p ${project_path}
if test ! -d "${project_path}/lib";then
        cp -r ${main_dir}/SF110-original/lib ${project_path}
fi


OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
counter=0

while read project_dir project_name class_name class_package other_features
do

	if [ $counter -eq 0  ];then
		counter=$((counter+1))
		continue;
	else
		mkdir ${results_directory}/${project_dir}-${class_package}
		mkdir ${results_directory}/logs
		logfile="${results_directory}/logs/mutation_analysis_logs_${run_number}.txt"

		echo | tee -a $logfile 2>&1
		echo "*********************************************************************************************************" | tee -a $logfile 2>&1
		echo "directory_name: ${project_dir} ****** project_name: ${project_name} ****** package_name: ${class_package}" | tee -a $logfile 2>&1
		echo "*********************************************************************************************************" | tee -a $logfile 2>&1
		if test -d "${project_path}/${project_dir}"; then
			rm -rf ${project_path}/${project_dir}
		fi
		
		cp -r ${main_dir}/SF110-original/${project_dir} ${project_path}
		lib_dir="${project_path}/${project_dir}/lib"
		
		#generating classpath string
		classpath="build/classes"
		number_jar=$(ls -lR ${lib_dir}/*.jar | wc -l)
		if [ $number_jar -gt 0 ];then
			for entry in ${lib_dir}/*.jar;
			do
				filename=$(basename $entry)
				#echo "$filename"
				classpath="${classpath}:lib/${filename}"
			done	
		fi
		echo "classpath: $classpath" | tee -a $logfile 2>&1

		
		cd "${main_dir}/${experiment_directory}/${project_dir}"

		#Delete all the files from last iteration (test generation and muttion analysis)
		if test -f "build-project.xml";then
			rm -f build.xml
			mv build-project.xml build.xml		
		fi
		
		rm -rf evosuite-report evosuite-tests build mutated_classes
		rm -f killed.csv killMap.csv mutants.log results.csv summary.csv testMap.csv template.mml template.mml.bin

		#compile project
		ant compile >> $logfile 2>&1
		
		#Making sure that compilation is successful before moving next
		ant_return_code=$?
		if [ $ant_return_code -ne 0 ];then
			echo "========ERROR========Error compiling $project_dir" | tee -a $logfile 2>&1
			continue
		else
	: '
'		
			# Rename evosuite-tests directory if it already exists
			if test -d "evosuite-tests";then
				mv evosuite-tests evosuite-tests-default
			fi

			#Generating evosuite tests			
			echo "========Generating Evosuite Testsuite========" | tee -a $logfile 2>&1		
			java -jar ${evosuite_path}/evosuite-1.1.0.jar -class ${class_package} -projectCP ${classpath} -Dshow_progress=false -Djunit_check=false -Dfilter_assertions=false -Dtest_comments=false -Duse_separate_classloader=true -Doutput_variables=TARGET_CLASS,algorithm,criterion,Total_Branches,Covered_Branches,BranchCoverage,Size,Length,Total_Goals,Covered_Goals -Dsearch_budget=120 -Dalgorithm=${evosuite_algo} -criterion branch -generateMOSuite >> $logfile 2>&1
			
			echo "========Test Generation Completed========" | tee -a $logfile 2>&1
			evosuite_return_code=$?

			if [ $evosuite_return_code -ne 0 ];then
				echo "========ERROR========Error occured while generating test suite for $project_dir: $class_package" | tee -a $logfile 2>&1
				continue
			else
				cp -r evosuite-report ${results_directory}/${project_dir}-${class_package}
				cp -r evosuite-tests ${results_directory}/${project_dir}-${class_package}
				
				cp $mml_path/template.mml ${main_dir}/${experiment_directory}/${project_dir}
				source ${SF110_scripts_path}/generate-mml.sh ${main_dir}/${experiment_directory}/${project_dir} $class_package
				${major_bin}/mmlc template.mml template.mml.bin
				mv build.xml build-project.xml

				#Adding major.compile, compile-evosuite-tests, mutation.test to build.xml
				source ${SF110_scripts_path}/addMutationTargetsToBuild.sh ${main_dir}/${experiment_directory}/${project_dir} ${major_bin}
				#compiling with major tool compiler to generate mutatns of the class based on mml file		
			  	ant -DmutOp="=template.mml.bin" major.compile >> $logfile 2>&1

				major_compile_return_code=$?
				if [ $major_compile_return_code -ne 0 ];then
					echo "========ERROR========Error occured while compiling using major compiler $project_dir: $class_package" | tee -a $logfile 2>&1
					continue
				else 

					#Running actual mutation analysis
					echo "========Starting Mutation Analysis========" | tee -a $logfile 2>&1				
					${major_bin}/ant mutation.test >> $logfile 2>&1
					echo "========Mutation Analysis Completed========" | tee -a $logfile 2>&1	
			
					major_mutation_return_code=$?
					if [ $major_mutation_return_code -ne 0 ];then
						echo "========ERROR========Error occured while doing mutation analysis $project_dir: $class_package" | tee -a $logfile 2>&1
						continue
					else
						mkdir ${results_directory}/${project_dir}-${class_package}/mutation-files
						cp killed.csv killMap.csv mutants.log results.csv summary.csv testMap.csv ${results_directory}/${project_dir}-${class_package}/mutation-files
					fi
				fi

			fi
		fi
	fi
	counter=$((counter+1))
done < $INPUT
IFS=$OLDIFS

