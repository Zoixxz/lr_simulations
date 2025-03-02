{
  tinypkgs ? import (fetchTarball {
    url = "https://gitlab.inria.fr/nix-tutorial/packages-repository/-/archive/master/packages-repository-8e43243635cd8f28c7213205b08c12f2ca2ac74d.tar.gz";
    sha256 = "sha256:09l2w3m1z0308zc476ci0bsz5amm536hj1n9xzpwcjm59jxkqpqa";
  }) {},
  pkgs ? import <nixpkgs> {}
}:

with tinypkgs; # Put tinypkgs's attributes in the current scope.
with pkgs; # Same for pkgs.

let
  pythonEnv = python312.withPackages (ps: with ps; [
    jupyter
    ipython
    numpy
    matplotlib
    pandas
    scipy
  ]);
in
mkShell {
  buildInputs = [
    chord
    
    pythonEnv # python env as specified above
    
    # C++ dev tools 
    tbb
    boost
    catch2_3
    clang-tools
    cmake
    ninja
  ];
  
  shellHook = ''
    export PS1="\[\033[01;32m\]nix-shell\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$ "
  '';
}