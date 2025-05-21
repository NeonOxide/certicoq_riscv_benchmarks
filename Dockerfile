
FROM	ocaml/opam:debian-ocaml-4.14
WORKDIR	/usr/local/certicoq
RUN	mkdir x86
RUN	mkdir riscv
RUN	sudo apt-get update
RUN	sudo apt-get install -y 	gcc-riscv64-linux-gnu gcc-riscv64-unknown-elf 	qemu-system-misc 	qemu-user 	ripgrep clang libgmp-dev linux-libc-dev pkg-config
RUN	opam install coq=8.19.2
RUN	opam install menhir
RUN	git clone -b v3.15 https://github.com/AbsInt/CompCert.git
WORKDIR	./CompCert
ENV	PATH	"$PATH:/home/opam/.opam/4.14/bin/"
RUN	./configure -ignore-coq-version x86_64-linux -bindir /usr/local/certicoq/x86/ -libdir /usr/local/certicoq/x86/ -sharedir /usr/local/certicoq/x86/
RUN	make clean
RUN	make all -j $(nproc)
RUN	sudo make install
RUN	make distclean
RUN	./configure -toolprefix riscv64-linux-gnu- -ignore-coq-version rv64-linux -bindir /usr/local/certicoq/riscv/ -libdir /usr/local/certicoq/riscv/ -sharedir /usr/local/certicoq/riscv/
RUN	make all -j $(nproc)
RUN	sudo make install
WORKDIR	../
RUN	git clone https://github.com/gem5/gem5
WORKDIR	./gem5
RUN	sudo apt-get install -y build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler  libprotoc-dev libgoogle-perftools-dev python3 python3-dev
RUN	scons build/X86/gem5.opt -j $(nproc)
RUN	scons build/RISCV/gem5.opt -j $(nproc)
WORKDIR	../
RUN	opam repo add coq-released https://coq.inria.fr/opam/released
RUN	opam install coq-certicoq
WORKDIR	$HOME
RUN	sudo apt-get -y install python3-rich
ADD	./certicoq	$HOME/certicoq
RUN	sudo mv /usr/local/certicoq/gem5 $HOME/gem5
ENV	GEM5_HOME	$HOME/gem5/
RUN	sudo chown -R opam $HOME/certicoq
RUN	sudo ln -s /usr/lib/gcc-cross/riscv64-linux-gnu/12/crtbeginT.o /usr/riscv64-linux-gnu/lib/crtbeginT.o
RUN	sudo apt-get install -y python3-pandas python3-seaborn
CMD	["/bin/bash"]
