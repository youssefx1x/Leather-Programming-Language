#include "../src/lth06/lth06.hpp"
#include <iostream>

int main() {
    using namespace leather::lth06;

    Program program = Compiler().make_demo_program();
    Result result = Runner().run(program);

    std::cout << "price = "
              << result.values.at("price").repr()
              << "\n";

    std::cout << "instructions = "
              << result.profile.instructions
              << "\n";

    std::cout << "specialization_hits = "
              << result.profile.specialization_hits
              << "\n";
}
