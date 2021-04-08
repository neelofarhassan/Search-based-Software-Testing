#!/bin/bash
project_path=$1
class_name=$2
cat >> $project_path/template.mml << EOF

// Enable operators for $class_name
AOR<"$class_name">;
LOR<"$class_name">;
SOR<"$class_name">;
COR<"$class_name">;
ROR<"$class_name">;
ORU<"$class_name">;
LVR<"$class_name">;
STD<"$class_name">;
EOF
