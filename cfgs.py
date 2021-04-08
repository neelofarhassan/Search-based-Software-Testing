import networkx as nx
import pydot
import numpy.linalg
import os
from os import path
import csv
import statistics
from networkx.drawing.nx_agraph import read_dot

def findAverageDegree(directedGraph):
	degrees = [val for (node, val) in directedGraph.degree()]
	print('********Node Degree******' , degrees)
	print('*****mean manually******' , float(sum(degrees)) / float(directedGraph.number_of_nodes()))
	return statistics.mean(degrees)

def findSTDEVDegree(directedGraph):
	degrees = [val for (node, val) in directedGraph.degree()]
	return statistics.pstdev(degrees)

def findMinimumDegree(directedGraph):
	degrees = [val for (node, val) in directedGraph.degree()]
	return  min(degrees)
		
def findMaximumDegree(directedGraph):
	degrees = [val for (node, val) in directedGraph.degree()]
	return  max(degrees)

#root directory containg projects (SF110 or Collections) and CFGs. We extracted CFGs using evosuite, which generate and save the CFGs in a directory under the project's main directory. 
home_dir="~/SF110-cfg"
#Output CSV
with open('~/graphfeatures.csv', 'w', newline='') as graph_features_file:
	writer = csv.writer(graph_features_file)
	writer.writerow(["Instances", "source", "feature_sum_num_cfs", "feature_avg_num_vertices", "feature_min_vertices", "feature_max_vertices", "feature_avg_num_edges", "feature_min_edges", "feature_max_edges", "feature_avg_radius", "feature_avg_diameter", "feature_avg_center_size", "feature_avg_periphery_size", "feature_avg_avg_shortest_path_length", "feature_avg_largest_eigenvalue_laplacian", "feature_avg_second_largest_eigenvalue_laplacian", "feature_avg_algebraic_connectivity", "feature_avg_eigenvalue_gap_laplacian", "feature_avg_graph_degree", "feature_avg_max_node_degree", "feature_avg_min_node_degree", "feature_avg_density", "feature_avg_edge_connectivity", "feature_avg_node_connectivity", "feature_avg_clustering_coefficient", "feature_avg_transitivity", "feature_avg_cfg_cyclomatic_complexity"])

	project_dirs = os.listdir(home_dir)
	id = 0
	for project_dir_name in project_dirs:
		project_name = ""
		project_package = ""
		class_name = ""
		identifier = ""
		source = "SF110"
		if os.path.isdir(os.path.join(home_dir,project_dir_name)):
			lib_dir_name = "lib"
			if(project_dir_name != 'lib'):
				project_dir_name_tokens = project_dir_name.split("_", 1)
				project_name = project_dir_name_tokens[1]
				cfg_dir = os.path.join(home_dir,project_dir_name,"evosuite-graphs")
				if path.exists(cfg_dir):
					print("***************************************************************************************")
					print("                            " + str(id) + ": " + project_dir_name + "                       ")
					print("***************************************************************************************")
					cfg_package_list = os.listdir(cfg_dir)
					for cfg_package in cfg_package_list:
						if "$" in cfg_package:
							continue
						id += 1
						identifier = project_name + "_" + cfg_package
						print ("project package: ", cfg_package)
						min_num_vertices = 0
						max_num_vertices = 0
						min_num_edges = 0
						max_num_edges = 0

						sum_num_cfs = 0.0
						sum_num_vertices = 0.0
						sum_num_edges = 0.0
						sum_radius = 0.0
						sum_diameter = 0.0
						sum_center_size = 0.0
						sum_periphery_size = 0.0
						sum_avg_shortest_path_length = 0.0
						sum_largest_eigenvalue_laplacian = 0.0
						sum_second_largest_eigenvalue_laplacian = 0.0
						sum_algebraic_connectivity = 0.0
						sum_eigenvalue_gap_laplacian = 0.0
						sum_energy = 0.0
						sum_graph_degree = 0.0
						sum_std_method_graph_degree = 0.0
						sum_max_node_degree = 0.0
						sum_min_node_degree = 0.0
						sum_density = 0.0
						sum_edge_connectivity = 0.0
						sum_node_connectivity = 0.0
						sum_clustering_coefficient = 0.0
						sum_transitivity = 0.0
						sum_cfg_cyclomatic_complexity = 0.0
						sum_class_complexity = 0.0

						avg_num_vertices = 0.0
						avg_num_edges = 0.0
						avg_radius = 0.0
						avg_diameter = 0.0
						avg_center_size = 0.0
						avg_periphery_size = 0.0
						avg_avg_shortest_path_length = 0.0
						avg_largest_eigenvalue_laplacian = 0.0
						avg_second_largest_eigenvalue_laplacian = 0.0
						avg_algebraic_connectivity = 0.0
						avg_eigenvalue_gap_laplacian = 0.0
						avg_energy = 0.0
						avg_graph_degree = 0.0
						avg_std_method_graph_degree = 0.0
						avg_max_node_degree = 0.0
						avg_min_node_degree = 0.0
						avg_density = 0.0
						avg_edge_connectivity = 0.0
						avg_node_connectivity = 0.0
						avg_clustering_coefficient = 0.0
						avg_transitivity = 0.0
						avg_cfg_cyclomatic_complexity = 0.0
						avg_class_complexity = 0.0

						num_edges_list = []
						num_vertices_list = []

						method_cfgs_path = os.path.join(cfg_dir, cfg_package, "ACFG")
						if path.exists(method_cfgs_path):
							method_cfgs_list = os.listdir(method_cfgs_path)
							num_cfg_methods = 0
							for cfg in method_cfgs_list:
								if cfg.endswith(".dot"):
									num_cfg_methods += 1

									num_vertices = 0.0
									num_edges = 0.0
									radius = 0.0
									diameter = 0.0
									center_size = 0.0
									periphery_size = 0.0
									avg_shortest_path_length = 0.0
									largest_eigenvalue_laplacian = 0.0
									second_largest_eigenvalue_laplacian = 0.0
									algebraic_connectivity = 0.0
									eigenvalue_gap_laplacian = 0.0
									energy = 0.0
									graph_degree = 0.0
									std_method_graph_degree = 0.0
									max_node_degree = 0.0
									min_node_degree = 0.0
									density = 0.0
									edge_connectivity = 0.0
									node_connectivity = 0.0
									clustering_coefficient = 0.0
									transitivity = 0.0
									cfg_cyclomatic_complexity = 0.0
									class_complexity = 0.0
									
									method_cfg_path = os.path.join(method_cfgs_path, cfg)
									print("****method name: ", method_cfg_path)
									DG = nx.DiGraph(nx.nx_pydot.read_dot(method_cfg_path))
									num_vertices = DG.number_of_nodes()
									sum_num_vertices = sum_num_vertices + num_vertices
									num_vertices_list.append(num_vertices)
									print("********Number of vertices: ", num_vertices)

									num_edges = DG.number_of_edges()
									sum_num_edges = sum_num_edges + num_edges
									num_edges_list.append(num_edges)
									print("********Number of edges: ", num_edges)

									UDG = DG.to_undirected()
									eccentricity = nx.eccentricity(UDG);
									#print("Eccentricity: " + str(eccentricity))
									radius = nx.radius(UDG, eccentricity)
									sum_radius = sum_radius + radius
									print("Radius: ", radius)

									diameter = nx.diameter(UDG, eccentricity)
									sum_diameter = sum_diameter + diameter
									print("Diameter: ", diameter)

									center_size_list = nx.center(UDG, eccentricity)
									center_size = len(center_size_list)
									sum_center_size = sum_center_size + center_size
									print("center: ", center_size)

									periphery_size_list = nx.periphery(UDG, eccentricity)
									periphery_size = len(periphery_size_list)
									sum_periphery_size = sum_periphery_size + periphery_size
									print("Periphery: ", periphery_size)

									density = nx.density(DG)
									sum_density = sum_density + density
									print("Density: ", density)

									edge_connectivity = nx.edge_connectivity(UDG)
									sum_edge_connectivity = sum_edge_connectivity + edge_connectivity
									print("Edge Connectivity UDG: ", edge_connectivity)

									node_connectivity = nx.node_connectivity(UDG)
									sum_node_connectivity = sum_node_connectivity + node_connectivity
									print("node Connectivity UDG: ", node_connectivity)

									clustering_coefficient = nx.average_clustering(DG)
									sum_clustering_coefficient = sum_clustering_coefficient + clustering_coefficient
									print("Average_clustering: ", clustering_coefficient)

									transitivity = nx.transitivity(DG)
									sum_transitivity = sum_transitivity + transitivity
									print("Transitivity: ", transitivity)

									UDG_number_of_nodes = UDG.number_of_nodes()
									UDG_number_of_edges = UDG.number_of_edges()
									number_of_connected_components = nx.number_connected_components(UDG)
									cfg_cyclomatic_complexity = float(UDG_number_of_edges - UDG_number_of_nodes + number_of_connected_components)
									sum_cfg_cyclomatic_complexity = sum_cfg_cyclomatic_complexity + cfg_cyclomatic_complexity
									print("cfg cyclomatic complexity: ", cfg_cyclomatic_complexity)

									avg_shortest_path_length = nx.average_shortest_path_length(DG)
									sum_avg_shortest_path_length = sum_avg_shortest_path_length + avg_shortest_path_length
									print("Average Shortest Length: ", avg_shortest_path_length)

									#Laplacian Features
									L = nx.normalized_laplacian_matrix(UDG)
									e = numpy.linalg.eigvals(L.A)
									idx_laplacian = e.argsort()[::-1]   
									sorted_e = e[idx_laplacian]
									largest_eigenvalue_laplacian = max(sorted_e)
									sum_largest_eigenvalue_laplacian = sum_largest_eigenvalue_laplacian + largest_eigenvalue_laplacian
									print("Largest eigenvalue of Laplacian:", largest_eigenvalue_laplacian)

									second_largest_eigenvalue_laplacian = sorted_e[1]
									sum_second_largest_eigenvalue_laplacian = sum_second_largest_eigenvalue_laplacian + second_largest_eigenvalue_laplacian
									print("Second Largest eigenvalue of Laplacian:",  second_largest_eigenvalue_laplacian)

									eigenvalue_gap_laplacian = largest_eigenvalue_laplacian - second_largest_eigenvalue_laplacian
									sum_eigenvalue_gap_laplacian = sum_eigenvalue_gap_laplacian + eigenvalue_gap_laplacian
									print("Eigenvalue Gap of Laplacian: ", eigenvalue_gap_laplacian)

									algebraic_connectivity = nx.algebraic_connectivity(UDG, method='lanczos')
									sum_algebraic_connectivity = sum_algebraic_connectivity + algebraic_connectivity
									print("Algebraic Connectivity: ", algebraic_connectivity)
									#print("eigenvalues list: " + str(sorted_e))


									#Adjacency Matrix Features
									adjacency_matrix = nx.adjacency_matrix(DG)
									#print("Adjacency Matrix: ", adjacency_matrix)
									eigenvalue_adjacency_matrix = numpy.linalg.eigvals(adjacency_matrix.A)
									#print("Eigenvaues of Adjacency Matrix: ", eigenvalue_adjacency_matrix)
									energy = eigenvalue_adjacency_matrix.mean()
									print("energy: ", energy)

									graph_degree = findAverageDegree(DG)
									sum_graph_degree = sum_graph_degree + graph_degree
									print("graph degree: ", graph_degree)

									std_method_graph_degree = findSTDEVDegree(DG)
									sum_std_method_graph_degree = sum_std_method_graph_degree + std_method_graph_degree
									print("Std method graph degree: " , std_method_graph_degree)

									min_node_degree = findMinimumDegree(DG)
									sum_min_node_degree = sum_min_node_degree + min_node_degree
									print("minimum degree:", min_node_degree)

									max_node_degree = findMaximumDegree(DG)
									sum_max_node_degree = sum_max_node_degree + max_node_degree
									print("maximum degree:", max_node_degree)

									sum_num_cfs = sum_num_cfs + num_cfg_methods


							avg_num_vertices = sum_num_vertices/num_cfg_methods
							avg_num_edges = sum_num_edges/num_cfg_methods
							avg_radius = sum_radius/num_cfg_methods
							avg_diameter = sum_diameter/num_cfg_methods
							avg_center_size = sum_center_size/num_cfg_methods
							avg_periphery_size = sum_periphery_size/num_cfg_methods
							avg_avg_shortest_path_length = sum_avg_shortest_path_length/num_cfg_methods
							avg_largest_eigenvalue_laplacian = sum_largest_eigenvalue_laplacian/num_cfg_methods
							avg_second_largest_eigenvalue_laplacian = sum_second_largest_eigenvalue_laplacian/num_cfg_methods
							avg_algebraic_connectivity = sum_algebraic_connectivity/num_cfg_methods
							avg_eigenvalue_gap_laplacian = sum_eigenvalue_gap_laplacian/num_cfg_methods
							avg_graph_degree = sum_graph_degree/num_cfg_methods
							avg_std_method_graph_degree = sum_std_method_graph_degree/num_cfg_methods
							avg_max_node_degree = sum_max_node_degree/num_cfg_methods
							avg_min_node_degree = sum_min_node_degree/num_cfg_methods
							avg_density = sum_density/num_cfg_methods
							avg_edge_connectivity = sum_edge_connectivity/num_cfg_methods
							avg_node_connectivity = sum_node_connectivity/num_cfg_methods
							avg_clustering_coefficient = sum_clustering_coefficient/num_cfg_methods
							avg_transitivity = sum_transitivity/num_cfg_methods
							min_edges = min(num_edges_list)
							max_edges = max(num_edges_list)
							min_vertices = min(num_vertices_list)
							max_vertices = max(num_vertices_list)
							avg_cfg_cyclomatic_complexity = sum_cfg_cyclomatic_complexity/num_cfg_methods


							writer.writerow([identifier, source, num_cfg_methods, avg_num_vertices, min_vertices, max_vertices, avg_num_edges, min_edges, max_edges, avg_radius, avg_diameter, avg_center_size, avg_periphery_size, avg_avg_shortest_path_length, avg_largest_eigenvalue_laplacian, avg_second_largest_eigenvalue_laplacian, avg_algebraic_connectivity, avg_eigenvalue_gap_laplacian, avg_graph_degree, avg_max_node_degree, avg_min_node_degree, avg_density, avg_edge_connectivity, avg_node_connectivity, avg_clustering_coefficient, avg_transitivity, avg_cfg_cyclomatic_complexity])

						else:
							print("ACFG doesnot exist for " + project_dir_name + "package: " +  cfg_package)
							


