#!/bin/bash
project_path=$1
major_compiler=$2
cat >> $project_path/build.xml << EOF
<project default="compile" basedir=".">
	<import file="build-project.xml" />

	<property name="mutOp" value=":NONE"/>	
	<!-- The directories for compilation targets -->
	<property name="tmp.classes"              value="temp_classes"/>
	<property name="mutated.classes"           value="mutated_classes"/>
	<path id="evosuite-1.1.0.lib">
		<pathelement location="\${lib.dir}/evosuite.jar" />
		<pathelement location="\${lib.dir}/hamcrest-core-1.3.jar" />
	</path> 

	<!-- ====================================================================== -->
	<target name="major.compile" description="Compile code with major compiler">
		<!-- Delete all previously mutated classes -->
		<delete dir="\${mutated.classes}" quiet="true" failonerror="false"/>

		<mkdir dir="\${tmp.classes}"/>
		<mkdir dir="\${mutated.classes}"/>

		<!-- Backup original class files (might not yet exist) -->
		<move file="\${build.classes}" tofile="\${tmp.classes}" quiet="true" failonerror="false"/>

		<mkdir dir="\${build.classes}"/>
		<javac  srcdir="\${source.java}"
		   destdir="\${build.classes}"
		    source="\${compile.source}"
		    target="\${compile.target}"
		     debug="\${compile.debug}"
		deprecation="\${compile.deprecation}"
		  optimize="\${compile.optimize}"
		  encoding="\${compile.encoding}"
		  fork="yes"
		  executable="${major_compiler}/javac">
		  	<compilerarg value="-XMutator\${mutOp}"/>
			<classpath refid="source.lib" />
		</javac>

		<copy todir="\${build.classes}">
			<fileset dir="\${source.java}" excludes="**/*.java"/>
			<fileset dir="\${source.resources}" includes="**"/>
		</copy>
		<!-- Move mutated classes to dedicated directory -->
		<move file="\${build.classes}" tofile="\${mutated.classes}"/>
		<!-- Restore original class files -->
		<move file="\${tmp.classes}" tofile="\${build.classes}" quiet="true" failonerror="false"/>
	</target>

	<!-- ====================================================================== -->
	  
	  <target name="compile-evosuite-tests"
		  description="Compile EvoSuite generated tests">
	    <mkdir dir="\${build.evosuite}"/>
	    <javac  srcdir="\${evosuite.java}"
		   destdir="\${build.evosuite}"
		    source="\${compile.source}"
		    target="\${compile.target}"
		     debug="\${compile.debug}"
	       deprecation="\${compile.deprecation}"
		  optimize="\${compile.optimize}">
		  <classpath>
		   <pathelement path="\${mutated.classes}"/> 
		   <path refid="source.lib" />
		    <path refid="test.lib" />
		    <path refid="evosuite-1.1.0.lib" />
		  </classpath>
	    </javac>
	  </target>

	<!-- ====================================================================== -->

	<target name="mutation.test" depends="compile-evosuite-tests"
	description="Run EvoSuite generated tests">
		<junit printsummary="false" 
			haltonfailure="no" 
			excludeFailingTests ="true"
			fork="yes"
			showoutput="false" 
			mutationAnalysis="true"
			summaryFile="summary.csv"
			resultFile="results.csv"
			killDetailsFile="killed.csv"
			exportKillMap="false">
			<formatter type="plain" usefile="false" />
		<classpath>
			<pathelement path="\${mutated.classes}"/>
			<pathelement path="\${build.evosuite}"/>
			<path refid="source.lib" />
			<path refid="test.lib" />
			<path refid="evosuite-1.1.0.lib" />
		</classpath>
		<batchtest fork="false">
			<fileset dir="\${evosuite.java}">
				<include name="**/*.java"/>
				<exclude name="**/*_scaffolding.java" />
			</fileset>
		</batchtest>
		</junit>
	</target> 
</project>
EOF
