#include <map>
#include <memory>
#include <stdexcept>
#include <functional>

#include <pybind11/pybind11.h>

typedef std::function< pybind11::module & (std::string const &) > ModuleGetter;

void bind_std_exception(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_std_unknown_unknown(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_std_unknown_unknown_1(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_CifFileReadDef(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_std___functional_base(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_std___locale(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_GenString(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_std___functional_base_1(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_GenString_1(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_rcsb_types(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_ITTable(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_ISTable(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_CifString(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_TableFile(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_DicFile(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_CifFileUtil(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_DataInfo(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_GenCont(std::function< pybind11::module &(std::string const &namespace_) > &M);
void bind_std_fstream(std::function< pybind11::module &(std::string const &namespace_) > &M);
//void bind_std_vector(std::function< pybind11::module &(std::string const &namespace_) > &M);


PYBIND11_MODULE(mmciflib, root_module) {
	root_module.doc() = "mmciflib module";

	std::map <std::string, pybind11::module> modules;
	ModuleGetter M = [&](std::string const &namespace_) -> pybind11::module & {
		auto it = modules.find(namespace_);
		if( it == modules.end() ) throw std::runtime_error("Attempt to access pybind11::module for namespace " + namespace_ + " before it was created!!!");
		return it->second;
	};

	modules[""] = root_module;

	std::vector< std::pair<std::string, std::string> > sub_modules {
		{"", "std"},
	};
	for(auto &p : sub_modules ) modules[p.first.size() ? p.first+"::"+p.second : p.second] = modules[p.first].def_submodule(p.second.c_str(), ("Bindings for " + p.first + "::" + p.second + " namespace").c_str() );

	//pybind11::class_<std::shared_ptr<void>>(M(""), "_encapsulated_data_");

	bind_std_exception(M);
	bind_std_unknown_unknown(M);
	bind_std_unknown_unknown_1(M);
	bind_CifFileReadDef(M);
	bind_std___functional_base(M);
	bind_std___locale(M);
	bind_GenString(M);
	bind_std___functional_base_1(M);
	bind_GenString_1(M);
	bind_rcsb_types(M);
	bind_ITTable(M);
	bind_ISTable(M);
	bind_CifString(M);
	bind_TableFile(M);
	bind_DicFile(M);
	bind_CifFileUtil(M);
	bind_DataInfo(M);
	bind_GenCont(M);
	bind_std_fstream(M);
	//bind_std_vector(M);

}
