#![allow(dead_code)]
#![allow(non_camel_case_types)]
#![allow(unused_imports)]
#![allow(non_snake_case)]
#![allow(unused_variables)]

use std::marker::PhantomData;

fn __nat_succ(x: u64) -> u64 {
  x.checked_add(1).unwrap()
}

macro_rules! __nat_elim {
    ($zcase:expr, $pred:ident, $scase:expr, $val:expr) => {
        { let v = $val;
        if v == 0 { $zcase } else { let $pred = v - 1; $scase } }
    }
}

macro_rules! __andb { ($b1:expr, $b2:expr) => { $b1 && $b2 } }
macro_rules! __orb { ($b1:expr, $b2:expr) => { $b1 || $b2 } }

fn __pos_onebit(x: u64) -> u64 {
  x.checked_mul(2).unwrap() + 1
}

fn __pos_zerobit(x: u64) -> u64 {
  x.checked_mul(2).unwrap()
}

macro_rules! __pos_elim {
    ($p:ident, $onebcase:expr, $p2:ident, $zerobcase:expr, $onecase:expr, $val:expr) => {
        {
            let n = $val;
            if n == 1 {
                $onecase
            } else if (n & 1) == 0 {
                let $p2 = n >> 1;
                $zerobcase
            } else {
                let $p = n >> 1;
                $onebcase
            }
        }
    }
}

fn __Z_frompos(z: u64) -> i64 {
  use std::convert::TryFrom;

  i64::try_from(z).unwrap()
}

fn __Z_fromneg(z : u64) -> i64 {
  use std::convert::TryFrom;

  i64::try_from(z).unwrap().checked_neg().unwrap()
}

macro_rules! __Z_elim {
    ($zero_case:expr, $p:ident, $pos_case:expr, $p2:ident, $neg_case:expr, $val:expr) => {
        {
            let n = $val;
            if n == 0 {
                $zero_case
            } else if n < 0 {
                let $p2 = n.unsigned_abs();
                $neg_case
            } else {
                let $p = n as u64;
                $pos_case
            }
        }
    }
}

fn __N_frompos(z: u64) -> u64 {
  z
}

macro_rules! __N_elim {
    ($zero_case:expr, $p:ident, $pos_case:expr, $val:expr) => {
        { let $p = $val; if $p == 0 { $zero_case } else { $pos_case } }
    }
}

type __pair<A, B> = (A, B);

macro_rules! __pair_elim {
    ($fst:ident, $snd:ident, $body:expr, $p:expr) => {
        { let ($fst, $snd) = $p; $body }
    }
}

fn __mk_pair<A: Copy, B: Copy>(a: A, b: B) -> __pair<A, B> { (a, b) }

fn hint_app<TArg, TRet>(f: &dyn Fn(TArg) -> TRet) -> &dyn Fn(TArg) -> TRet {
  f
}

#[derive(Debug, Clone)]
pub enum Coq_Init_Datatypes_list<'a, A> {
  nil(PhantomData<&'a A>),
  cons(PhantomData<&'a A>, A, &'a Coq_Init_Datatypes_list<'a, A>)
}

struct Program {
  __alloc: bumpalo::Bump,
}

impl<'a> Program {
fn new() -> Self {
  Program {
    __alloc: bumpalo::Bump::new(),
  }
}

fn alloc<T>(&'a self, t: T) -> &'a T {
  self.__alloc.alloc(t)
}

fn closure<TArg, TRet>(&'a self, F: impl Fn(TArg) -> TRet + 'a) -> &'a dyn Fn(TArg) -> TRet {
  self.__alloc.alloc(F)
}

fn Coq_Lists_List_map<A: Copy, B: Copy>(&'a self, f: &'a dyn Fn(A) -> B, l: &'a Coq_Init_Datatypes_list<'a, A>) -> &'a Coq_Init_Datatypes_list<'a, B> {
  match l {
    &Coq_Init_Datatypes_list::nil(_) => {
      self.alloc(
        Coq_Init_Datatypes_list::nil(
          PhantomData))
    },
    &Coq_Init_Datatypes_list::cons(_, a, t) => {
      self.alloc(
        Coq_Init_Datatypes_list::cons(
          PhantomData,
          hint_app(f)(a),
          self.Coq_Lists_List_map(
            f,
            t)))
    },
  }
}
fn Coq_Lists_List_map__curried<A: Copy, B: Copy>(&'a self) -> &'a dyn Fn(&'a dyn Fn(A) -> B) -> &'a dyn Fn(&'a Coq_Init_Datatypes_list<'a, A>) -> &'a Coq_Init_Datatypes_list<'a, B> {
  self.closure(move |f| {
    self.closure(move |l| {
      self.Coq_Lists_List_map(
        f,
        l)
    })
  })
}

fn Coq_Init_Datatypes_negb(&'a self, b: bool) -> bool {
  match b {
    true => {
      false
    },
    false => {
      true
    },
  }
}
fn Coq_Init_Datatypes_negb__curried(&'a self) -> &'a dyn Fn(bool) -> bool {
  self.closure(move |b| {
    self.Coq_Init_Datatypes_negb(
      b)
  })
}

fn CertiCoq_Benchmarks_rust_tests_repeat2<A: Copy>(&'a self, A: (), x: A, y: A, n: u64) -> &'a Coq_Init_Datatypes_list<'a, A> {
  __nat_elim!(
    {
      self.alloc(
        Coq_Init_Datatypes_list::nil(
          PhantomData))
    },
    n2, {
      self.alloc(
        Coq_Init_Datatypes_list::cons(
          PhantomData,
          x,
          self.alloc(
            Coq_Init_Datatypes_list::cons(
              PhantomData,
              y,
              self.CertiCoq_Benchmarks_rust_tests_repeat2(
                (),
                x,
                y,
                n2)))))
    },
    n)
}
fn CertiCoq_Benchmarks_rust_tests_repeat2__curried<A: Copy>(&'a self) -> &'a dyn Fn(()) -> &'a dyn Fn(A) -> &'a dyn Fn(A) -> &'a dyn Fn(u64) -> &'a Coq_Init_Datatypes_list<'a, A> {
  self.closure(move |A| {
    self.closure(move |x| {
      self.closure(move |y| {
        self.closure(move |n| {
          self.CertiCoq_Benchmarks_rust_tests_repeat2(
            A,
            x,
            y,
            n)
        })
      })
    })
  })
}

fn CertiCoq_Benchmarks_rust_tests_demo2(&'a self) -> &'a Coq_Init_Datatypes_list<'a, bool> {
  self.Coq_Lists_List_map(
    self.Coq_Init_Datatypes_negb__curried(),
    self.CertiCoq_Benchmarks_rust_tests_repeat2(
      (),
      true,
      false,
      __nat_succ(
        __nat_succ(
          __nat_succ(
            __nat_succ(
              __nat_succ(
                __nat_succ(
                  __nat_succ(
                    __nat_succ(
                      __nat_succ(
                        __nat_succ(
                          __nat_succ(
                            __nat_succ(
                              __nat_succ(
                                __nat_succ(
                                  __nat_succ(
                                    __nat_succ(
                                      __nat_succ(
                                        __nat_succ(
                                          __nat_succ(
                                            __nat_succ(
                                              __nat_succ(
                                                __nat_succ(
                                                  __nat_succ(
                                                    __nat_succ(
                                                      __nat_succ(
                                                        __nat_succ(
                                                          __nat_succ(
                                                            __nat_succ(
                                                              __nat_succ(
                                                                __nat_succ(
                                                                  __nat_succ(
                                                                    __nat_succ(
                                                                      __nat_succ(
                                                                        __nat_succ(
                                                                          __nat_succ(
                                                                            __nat_succ(
                                                                              __nat_succ(
                                                                                __nat_succ(
                                                                                  __nat_succ(
                                                                                    __nat_succ(
                                                                                      __nat_succ(
                                                                                        __nat_succ(
                                                                                          __nat_succ(
                                                                                            __nat_succ(
                                                                                              __nat_succ(
                                                                                                __nat_succ(
                                                                                                  __nat_succ(
                                                                                                    __nat_succ(
                                                                                                      __nat_succ(
                                                                                                        __nat_succ(
                                                                                                          __nat_succ(
                                                                                                            __nat_succ(
                                                                                                              __nat_succ(
                                                                                                                __nat_succ(
                                                                                                                  __nat_succ(
                                                                                                                    __nat_succ(
                                                                                                                      __nat_succ(
                                                                                                                        __nat_succ(
                                                                                                                          __nat_succ(
                                                                                                                            __nat_succ(
                                                                                                                              __nat_succ(
                                                                                                                                __nat_succ(
                                                                                                                                  __nat_succ(
                                                                                                                                    __nat_succ(
                                                                                                                                      __nat_succ(
                                                                                                                                        __nat_succ(
                                                                                                                                          __nat_succ(
                                                                                                                                            __nat_succ(
                                                                                                                                              __nat_succ(
                                                                                                                                                __nat_succ(
                                                                                                                                                  __nat_succ(
                                                                                                                                                    __nat_succ(
                                                                                                                                                      __nat_succ(
                                                                                                                                                        __nat_succ(
                                                                                                                                                          __nat_succ(
                                                                                                                                                            __nat_succ(
                                                                                                                                                              __nat_succ(
                                                                                                                                                                __nat_succ(
                                                                                                                                                                  __nat_succ(
                                                                                                                                                                    __nat_succ(
                                                                                                                                                                      __nat_succ(
                                                                                                                                                                        __nat_succ(
                                                                                                                                                                          __nat_succ(
                                                                                                                                                                            __nat_succ(
                                                                                                                                                                              __nat_succ(
                                                                                                                                                                                __nat_succ(
                                                                                                                                                                                  __nat_succ(
                                                                                                                                                                                    __nat_succ(
                                                                                                                                                                                      __nat_succ(
                                                                                                                                                                                        __nat_succ(
                                                                                                                                                                                          __nat_succ(
                                                                                                                                                                                            __nat_succ(
                                                                                                                                                                                              __nat_succ(
                                                                                                                                                                                                __nat_succ(
                                                                                                                                                                                                  __nat_succ(
                                                                                                                                                                                                    __nat_succ(
                                                                                                                                                                                                      __nat_succ(
                                                                                                                                                                                                        __nat_succ(
                                                                                                                                                                                                          __nat_succ(
                                                                                                                                                                                                            __nat_succ(
                                                                                                                                                                                                              0))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
}
}
