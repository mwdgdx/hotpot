failing in linux with logging
```
| eval      7 in epoch   0 | time: 873.61s | dev loss    5.752 | EM 34.4767 | F1 46.9200
-----------------------------------------------------------------------------------------
| epoch   0 | step   7100 | lr 0.10000 | ms/batch 2649.37 | train loss    4.485
*** Error in `python': double free or corruption (fasttop): 0x00007f5d203fc2b0 ***
======= Backtrace: =========
/lib/x86_64-linux-gnu/libc.so.6(+0x777e5)[0x7f5eee2c17e5]
/lib/x86_64-linux-gnu/libc.so.6(+0x8037a)[0x7f5eee2ca37a]
/lib/x86_64-linux-gnu/libc.so.6(cfree+0x4c)[0x7f5eee2ce53c]
/usr/lib/x86_64-linux-gnu/libcuda.so.1(+0x1f9bbf)[0x7f5ec2196bbf]
/usr/lib/x86_64-linux-gnu/libcuda.so.1(+0x108612)[0x7f5ec20a5612]
/usr/lib/x86_64-linux-gnu/libcuda.so.1(+0x1086d0)[0x7f5ec20a56d0]
/usr/lib/x86_64-linux-gnu/libcuda.so.1(cuStreamCreateWithPriority+0x61)[0x7f5ec21d3501]
/usr/local/lib/python3.5/dist-packages/torch/lib/libcudart-f7fdd8d7.so.9.0(+0x15b62)[0x7f5e83b0db62]
/usr/local/lib/python3.5/dist-packages/torch/lib/libcudart-f7fdd8d7.so.9.0(+0x15c3e)[0x7f5e83b0dc3e]
/usr/local/lib/python3.5/dist-packages/torch/lib/libcudart-f7fdd8d7.so.9.0(cudaStreamCreate+0x67)[0x7f5e83b3cd07]
/usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so(_ZN17RNNBackwardFilterIfffE4initEP12cudnnContextP14cudnnRNNStructi11PerfOptions+0x3b0)[0x7f5e94f679d0]
/usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so(cudnnRNNBackwardWeights+0xead)[0x7f5e94f66bcd]
/usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so(_ZN2at6native26_cudnn_rnn_backward_weightERKNS_6TensorEN3c108ArrayRefIS1_EElS3_S3_S3_S3_lllbdbbNS5_IlEES3_S3_+0xb85)[0x7f5e9053e965]
/usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so(_ZN2at6native19_cudnn_rnn_backwardERKNS_6TensorEN3c108ArrayRefIS1_EElS3_S3_S3_S3_S3_S3_S3_lllbdbbNS5_IlEES3_S3_St5arrayIbLm4EE+0x2f6)[0x7f5e905446e6]
/usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so(_ZNK2at13CUDAFloatType19_cudnn_rnn_backwardERKNS_6TensorEN3c108ArrayRefIS1_EElS3_S3_S3_S3_S3_S3_S3_lllbdbbNS5_IlEES3_S3_St5arrayIbLm4EE+0xfb)[0x7f5e906008db]
/usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1(_ZNK5torch8autograd12VariableType19_cudnn_rnn_backwardERKN2at6TensorEN3c108ArrayRefIS3_EElS5_S5_S5_S5_S5_S5_S5_lllbdbbNS7_IlEES5_S5_St5arrayIbLm4EE+0x338)[0x7f5e84338a08]
/usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1(_ZN5torch8autograd9generated16CudnnRnnBackward5applyEOSt6vectorINS0_8VariableESaIS4_EE+0x654)[0x7f5e842429c4]
/usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1(_ZN5torch8autograd6Engine17evaluate_functionERNS0_12FunctionTaskE+0x39e)[0x7f5e8421a6ee]
/usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1(_ZN5torch8autograd6Engine11thread_mainEPNS0_9GraphTaskE+0xc0)[0x7f5e8421c850]
/usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1(_ZN5torch8autograd6Engine11thread_initEi+0xc7)[0x7f5e84219377]
/usr/local/lib/python3.5/dist-packages/torch/lib/libtorch_python.so(_ZN5torch8autograd6python12PythonEngine11thread_initEi+0x2a)[0x7f5ebf69bdfa]
/usr/lib/x86_64-linux-gnu/libstdc++.so.6(+0xb8c80)[0x7f5ec6eddc80]
/lib/x86_64-linux-gnu/libpthread.so.0(+0x76ba)[0x7f5eee61b6ba]
/lib/x86_64-linux-gnu/libc.so.6(clone+0x6d)[0x7f5eee35141d]
======= Memory map: ========
00400000-007a9000 r-xp 00000000 08:17 3019826                            /usr/bin/python3.5
009a9000-009ab000 r--p 003a9000 08:17 3019826                            /usr/bin/python3.5
009ab000-00a42000 rw-p 003ab000 08:17 3019826                            /usr/bin/python3.5
00a42000-00a73000 rw-p 00000000 00:00 0
0233d000-7e8fca000 rw-p 00000000 00:00 0                                 [heap]
800000000-800200000 rw-s 00000000 00:06 520                              /dev/nvidiactl
800200000-800400000 ---p 00000000 00:00 0
800400000-800404000 rw-s 00000000 00:06 520                              /dev/nvidiactl
800404000-800600000 ---p 00000000 00:00 0
800600000-800a00000 rw-s 00000000 00:06 520                              /dev/nvidiactl
800a00000-801600000 ---p 00000000 00:00 0
801600000-801800000 rw-s 00000000 00:06 520                              /dev/nvidiactl
801800000-801804000 rw-s 00000000 00:06 520                              /dev/nvidiactl
801804000-801a00000 ---p 00000000 00:00 0
801a00000-801e00000 rw-s 00000000 00:06 520                              /dev/nvidiactl
801e00000-801e04000 rw-s 00000000 00:06 520                              /dev/nvidiactl
801e04000-802000000 ---p 00000000 00:00 0
802000000-802400000 rw-s 00000000 00:06 520                              /dev/nvidiactl
802400000-802404000 rw-s 00000000 00:06 520                              /dev/nvidiactl
802404000-802600000 ---p 00000000 00:00 0
802600000-802a00000 rw-s 00000000 00:06 520                              /dev/nvidiactl
802a00000-802a04000 rw-s 00000000 00:06 520                              /dev/nvidiactl
802a04000-802c00000 ---p 00000000 00:00 0
802c00000-803000000 rw-s 00000000 00:06 520                              /dev/nvidiactl
803000000-803004000 rw-s 00000000 00:06 520                              /dev/nvidiactl
803004000-803200000 ---p 00000000 00:00 0
803200000-803600000 rw-s 00000000 00:06 520                              /dev/nvidiactl
803600000-803604000 rw-s 00000000 00:06 520                              /dev/nvidiactl
803604000-803800000 ---p 00000000 00:00 0
803800000-803c00000 rw-s 00000000 00:06 520                              /dev/nvidiactl
803c00000-803c04000 rw-s 00000000 00:06 520                              /dev/nvidiactl
803c04000-803e00000 ---p 00000000 00:00 0
803e00000-804200000 rw-s 00000000 00:06 520                              /dev/nvidiactl
804200000-804204000 rw-s 00000000 00:06 520                              /dev/nvidiactl
804204000-804400000 ---p 00000000 00:00 0
804400000-804800000 rw-s 00000000 00:06 520                              /dev/nvidiactl
804800000-804804000 rw-s 00000000 00:06 520                              /dev/nvidiactl
804804000-804a00000 ---p 00000000 00:00 0
804a00000-804e00000 rw-s 00000000 00:06 520                              /dev/nvidiactl
804e00000-804e04000 rw-s 00000000 00:06 520                              /dev/nvidiactl
804e04000-805000000 ---p 00000000 00:00 0
805000000-805400000 rw-s 00000000 00:06 520                              /dev/nvidiactl
805400000-805404000 rw-s 00000000 00:06 520                              /dev/nvidiactl
805404000-805600000 ---p 00000000 00:00 0
805600000-805a00000 rw-s 00000000 00:06 520                              /dev/nvidiactl
805a00000-805a04000 rw-s 00000000 00:06 520                              /dev/nvidiactl
805a04000-805c00000 ---p 00000000 00:00 0
805c00000-806000000 rw-s 00000000 00:06 520                              /dev/nvidiactl
806000000-806004000 rw-s 00000000 00:06 520                              /dev/nvidiactl
806004000-806200000 ---p 00000000 00:00 0
806200000-806600000 rw-s 00000000 00:06 520                              /dev/nvidiactl
806600000-806604000 rw-s 00000000 00:06 520                              /dev/nvidiactl
806604000-806800000 ---p 00000000 00:00 0
806800000-806c00000 rw-s 00000000 00:06 520                              /dev/nvidiactl
806c00000-806c04000 rw-s 00000000 00:06 520                              /dev/nvidiactl
806c04000-806e00000 ---p 00000000 00:00 0
806e00000-807200000 rw-s 00000000 00:06 520                              /dev/nvidiactl
807200000-807400000 ---p 00000000 00:00 0
807400000-807600000 rw-s 00000000 00:06 520                              /dev/nvidiactl
807600000-900200000 ---p 00000000 00:00 0
10000000000-10204000000 ---p 00000000 00:00 0
7f5aae000000-7f5aee000000 ---p 00000000 00:00 0
7f5b56000000-7f5b86000000 ---p 00000000 00:00 0
7f5c3e000000-7f5c4c000000 ---p 00000000 00:00 0
7f5c68000000-7f5c76000000 ---p 00000000 00:00 0
7f5cae000000-7f5cb8000000 ---p 00000000 00:00 0
7f5ce8000000-7f5d18000000 ---p 00000000 00:00 0
7f5d18000000-7f5d18021000 rw-p 00000000 00:00 0
7f5d18021000-7f5d1c000000 ---p 00000000 00:00 0
7f5d1c000000-7f5d1c021000 rw-p 00000000 00:00 0
7f5d1c021000-7f5d20000000 ---p 00000000 00:00 0
7f5d20000000-7f5d2042b000 rw-p 00000000 00:00 0
7f5d2042b000-7f5d24000000 ---p 00000000 00:00 0
7f5d28000000-7f5d58000000 ---p 00000000 00:00 0
7f5d59b5d000-7f5d59b9d000 rw-p 00000000 00:00 0
7f5d5c000000-7f5d64000000 ---p 00000000 00:00 0
7f5d6a000000-7f5d92a00000 ---p 00000000 00:00 0
7f5d92a00000-7f5d92c00000 rw-s 00000000 00:05 8367078                    /dev/zero (deleted)
7f5d92c00000-7f5d94000000 ---p 00000000 00:00 0
7f5d9502a000-7f5d98b9f000 rw-p 00000000 00:00 0
7f5d9c714000-7f5d9e000000 rw-p 00000000 00:00 0
7f5d9e000000-7f5da5600000 ---p 00000000 00:00 0
7f5da5600000-7f5da5800000 rw-s 00000000 00:05 8367072                    /dev/zero (deleted)
7f5da5800000-7f5da8000000 ---p 00000000 00:00 0
7f5da8000000-7f5da8021000 rw-p 00000000 00:00 0
7f5da8021000-7f5dac000000 ---p 00000000 00:00 0
7f5dac000000-7f5dac021000 rw-p 00000000 00:00 0
7f5dac021000-7f5db0000000 ---p 00000000 00:00 0
7f5db0000000-7f5db0001000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0001000-7f5db0002000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0002000-7f5db0003000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0003000-7f5db0004000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0004000-7f5db0005000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0005000-7f5db0006000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0006000-7f5db0007000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0007000-7f5db0008000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0008000-7f5db0009000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0009000-7f5db000a000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db000a000-7f5db000b000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db000b000-7f5db000c000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db000c000-7f5db000d000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db000d000-7f5db000e000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db000e000-7f5db000f000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db000f000-7f5db0010000 rw-s 00000000 00:06 521                        /dev/nvidia0
7f5db0010000-7f5dc0000000 ---p 00000000 00:00 0
7f5dc2b64000-7f5dc8b64000 ---p 00000000 00:00 0
7f5dcc000000-7f5de1000000 ---p 00000000 00:00 0
7f5de1000000-7f5de1200000 rw-s 00000000 00:05 8367091                    /dev/zero (deleted)
7f5de1200000-7f5de4000000 ---p 00000000 00:00 0
7f5de4fbc000-7f5de597c000 rw-p 00000000 00:00 0
7f5de717d000-7f5df72bd000 rw-p 00000000 00:00 0
7f5df8000000-7f5df8200000 ---p 00000000 00:00 0
7f5df8200000-7f5df8400000 rw-s 00000000 00:05 8351063                    /dev/zero (deleted)
7f5df8400000-7f5df8600000 rw-s 00000000 00:06 520                        /dev/nvidiactl
7f5df8600000-7f5df8800000 rw-s 00000000 00:05 8351064                    /dev/zero (deleted)
7f5df8800000-7f5df8a00000 rw-s 00000000 00:06 520                        /dev/nvidiactl
7f5df8a00000-7f5df8c00000 ---p 00000000 00:00 0
7f5df8c00000-7f5df8ed6000 rw-s 00000000 00:06 520                        /dev/nvidiactl
7f5df8ed6000-7f5dfa000000 ---p 00000000 00:00 0
7f5dfaabd000-7f5dfaabe000 ---p 00000000 00:00 0
7f5dfaabe000-7f5e3fd3e000 rw-p 00000000 00:00 0
7f5e3fd4b000-7f5e4618b000 rw-p 00000000 00:00 0
7f5e4618c000-7f5e5010c000 rw-p 00000000 00:00 0
7f5e5010d000-7f5e5438d000 rw-p 00000000 00:00 0
7f5e5438e000-7f5e5934e000 rw-p 00000000 00:00 0
7f5e5934f000-7f5e5d98f000 rw-p 00000000 00:00 0
7f5e5d990000-7f5e5fe90000 rw-p 00000000 00:00 0
7f5e5fe91000-7f5e81229000 rw-p 00000000 00:00 0
7f5e81229000-7f5e81256000 r-xp 00000000 08:17 3151822                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/ner.cpython-35m-x86_64-linux-gnu.so
7f5e81256000-7f5e81456000 ---p 0002d000 08:17 3151822                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/ner.cpython-35m-x86_64-linux-gnu.so
7f5e81456000-7f5e81459000 rw-p 0002d000 08:17 3151822                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/ner.cpython-35m-x86_64-linux-gnu.so
7f5e81459000-7f5e814a9000 r-xp 00000000 08:17 3151815                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/_beam_utils.cpython-35m-x86_64-linux-gnu.so
7f5e814a9000-7f5e816a9000 ---p 00050000 08:17 3151815                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/_beam_utils.cpython-35m-x86_64-linux-gnu.so
7f5e816a9000-7f5e816ae000 rw-p 00050000 08:17 3151815                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/_beam_utils.cpython-35m-x86_64-linux-gnu.so
7f5e816ae000-7f5e816af000 rw-p 00000000 00:00 0
7f5e816af000-7f5e816cd000 r-xp 00000000 08:17 3149381                    /usr/local/lib/python3.5/dist-packages/thinc/extra/search.cpython-35m-x86_64-linux-gnu.so
7f5e816cd000-7f5e818cc000 ---p 0001e000 08:17 3149381                    /usr/local/lib/python3.5/dist-packages/thinc/extra/search.cpython-35m-x86_64-linux-gnu.so
7f5e818cc000-7f5e818cf000 rw-p 0001d000 08:17 3149381                    /usr/local/lib/python3.5/dist-packages/thinc/extra/search.cpython-35m-x86_64-linux-gnu.so
7f5e818cf000-7f5e81900000 r-xp 00000000 08:17 3151833                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/arc_eager.cpython-35m-x86_64-linux-gnu.so
7f5e81900000-7f5e81b00000 ---p 00031000 08:17 3151833                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/arc_eager.cpython-35m-x86_64-linux-gnu.so
7f5e81b00000-7f5e81b03000 rw-p 00031000 08:17 3151833                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/arc_eager.cpython-35m-x86_64-linux-gnu.so
7f5e81b03000-7f5e81bb4000 r-xp 00000000 08:17 3151835                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/nn_parser.cpython-35m-x86_64-linux-gnu.so
7f5e81bb4000-7f5e81db3000 ---p 000b1000 08:17 3151835                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/nn_parser.cpython-35m-x86_64-linux-gnu.so
7f5e81db3000-7f5e81dbc000 rw-p 000b0000 08:17 3151835                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/nn_parser.cpython-35m-x86_64-linux-gnu.so
7f5e81dbc000-7f5e81dbe000 rw-p 00000000 00:00 0
7f5e81dbe000-7f5e81e6f000 r-xp 00000000 08:17 3149901                    /usr/local/lib/python3.5/dist-packages/spacy/pipeline.cpython-35m-x86_64-linux-gnu.so
7f5e81e6f000-7f5e8206e000 ---p 000b1000 08:17 3149901                    /usr/local/lib/python3.5/dist-packages/spacy/pipeline.cpython-35m-x86_64-linux-gnu.so
7f5e8206e000-7f5e82079000 rw-p 000b0000 08:17 3149901                    /usr/local/lib/python3.5/dist-packages/spacy/pipeline.cpython-35m-x86_64-linux-gnu.so
7f5e82079000-7f5e8207b000 rw-p 00000000 00:00 0
7f5e8207b000-7f5e820aa000 r-xp 00000000 08:17 3149928                    /usr/local/lib/python3.5/dist-packages/spacy/tokenizer.cpython-35m-x86_64-linux-gnu.so
7f5e820aa000-7f5e822a9000 ---p 0002f000 08:17 3149928                    /usr/local/lib/python3.5/dist-packages/spacy/tokenizer.cpython-35m-x86_64-linux-gnu.so
7f5e822a9000-7f5e822ad000 rw-p 0002e000 08:17 3149928                    /usr/local/lib/python3.5/dist-packages/spacy/tokenizer.cpython-35m-x86_64-linux-gnu.so
7f5e822ad000-7f5e82e6f000 rw-p 00000000 00:00 0
7f5e82e70000-7f5e83330000 rw-p 00000000 00:00 0
7f5e83330000-7f5e83333000 r-xp 00000000 08:17 2895771                    /usr/lib/python3.5/lib-dynload/_multiprocessing.cpython-35m-x86_64-linux-gnu.so
7f5e83333000-7f5e83532000 ---p 00003000 08:17 2895771                    /usr/lib/python3.5/lib-dynload/_multiprocessing.cpython-35m-x86_64-linux-gnu.so
7f5e83532000-7f5e83533000 r--p 00002000 08:17 2895771                    /usr/lib/python3.5/lib-dynload/_multiprocessing.cpython-35m-x86_64-linux-gnu.so
7f5e83533000-7f5e83534000 rw-p 00003000 08:17 2895771                    /usr/lib/python3.5/lib-dynload/_multiprocessing.cpython-35m-x86_64-linux-gnu.so
7f5e83534000-7f5e838f4000 rw-p 00000000 00:00 0
7f5e838f4000-7f5e838f5000 r-xp 00000000 08:17 3680610                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10_cuda.so
7f5e838f5000-7f5e83af4000 ---p 00001000 08:17 3680610                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10_cuda.so
7f5e83af4000-7f5e83af5000 r--p 00000000 08:17 3680610                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10_cuda.so
7f5e83af5000-7f5e83af8000 rw-p 00001000 08:17 3680610                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10_cuda.so
7f5e83af8000-7f5e83b61000 r-xp 00000000 08:17 3680616                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcudart-f7fdd8d7.so.9.0
7f5e83b61000-7f5e83d60000 ---p 00069000 08:17 3680616                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcudart-f7fdd8d7.so.9.0
7f5e83d60000-7f5e83d64000 rw-p 00068000 08:17 3680616                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcudart-f7fdd8d7.so.9.0
7f5e83d64000-7f5e83d65000 rw-p 00000000 00:00 0
7f5e83d65000-7f5e83d68000 rw-p 0006d000 08:17 3680616                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcudart-f7fdd8d7.so.9.0
7f5e83d68000-7f5e83d70000 r-xp 00000000 08:17 3680618                    /usr/local/lib/python3.5/dist-packages/torch/lib/libnvToolsExt-3965bdd0.so.1
7f5e83d70000-7f5e83f70000 ---p 00008000 08:17 3680618                    /usr/local/lib/python3.5/dist-packages/torch/lib/libnvToolsExt-3965bdd0.so.1
7f5e83f70000-7f5e83f71000 rw-p 00008000 08:17 3680618                    /usr/local/lib/python3.5/dist-packages/torch/lib/libnvToolsExt-3965bdd0.so.1
7f5e83f71000-7f5e83f72000 rw-p 0000a000 08:17 3680618                    /usr/local/lib/python3.5/dist-packages/torch/lib/libnvToolsExt-3965bdd0.so.1
7f5e83f72000-7f5e84ab7000 r-xp 00000000 08:17 3680625                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1
7f5e84ab7000-7f5e84cb6000 ---p 00b45000 08:17 3680625                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1
7f5e84cb6000-7f5e84cf3000 r--p 00b44000 08:17 3680625                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1
7f5e84cf3000-7f5e84cf8000 rw-p 00b81000 08:17 3680625                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1
7f5e84cf8000-7f5e84cfb000 rw-p 00000000 00:00 0
7f5e84cfb000-7f5e84f29000 rw-p 00e66000 08:17 3680625                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch.so.1
7f5e84f29000-7f5e84f4e000 r-xp 00000000 08:17 3680617                    /usr/local/lib/python3.5/dist-packages/torch/lib/libgomp-8bba0e50.so.1
7f5e84f4e000-7f5e8514d000 ---p 00025000 08:17 3680617                    /usr/local/lib/python3.5/dist-packages/torch/lib/libgomp-8bba0e50.so.1
7f5e8514d000-7f5e8514e000 r--p 00024000 08:17 3680617                    /usr/local/lib/python3.5/dist-packages/torch/lib/libgomp-8bba0e50.so.1
7f5e8514e000-7f5e85153000 rw-p 00025000 08:17 3680617                    /usr/local/lib/python3.5/dist-packages/torch/lib/libgomp-8bba0e50.so.1
7f5e85153000-7f5e85170000 r-xp 00000000 08:17 3680609                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10.so
7f5e85170000-7f5e85370000 ---p 0001d000 08:17 3680609                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10.so
7f5e85370000-7f5e85371000 r--p 0001d000 08:17 3680609                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10.so
7f5e85371000-7f5e85372000 rw-p 0001e000 08:17 3680609                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10.so
7f5e85372000-7f5e85373000 rw-p 00000000 00:00 0
7f5e85373000-7f5e85377000 rw-p 0002b000 08:17 3680609                    /usr/local/lib/python3.5/dist-packages/torch/lib/libc10.so
7f5e85377000-7f5e8eab0000 r-xp 00000000 08:17 3680611                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2.so
7f5e8eab0000-7f5e8ecaf000 ---p 09739000 08:17 3680611                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2.so
7f5e8ecaf000-7f5e8eda0000 r--p 09738000 08:17 3680611                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2.so
7f5e8eda0000-7f5e8eef9000 rw-p 09829000 08:17 3680611                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2.so
7f5e8eef9000-7f5e8ef6b000 rw-p 00000000 00:00 0
7f5e8ef6b000-7f5e8f2f4000 rw-p 0a6a2000 08:17 3680611                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2.so
7f5e8f2f4000-7f5ebbfbc000 r-xp 00000000 08:17 3680613                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so
7f5ebbfbc000-7f5ebc1bc000 ---p 2ccc8000 08:17 3680613                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so
7f5ebc1bc000-7f5ebc2d9000 r--p 2ccc8000 08:17 3680613                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so
7f5ebc2d9000-7f5ebd6f4000 rw-p 2cde5000 08:17 3680613                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so
7f5ebd6f4000-7f5ebdde4000 rw-p 00000000 00:00 0
7f5ebdde4000-7f5ebf392000 rw-p 311fb000 08:17 3680613                    /usr/local/lib/python3.5/dist-packages/torch/lib/libcaffe2_gpu.so
7f5ebf392000-7f5ebfb94000 r-xp 00000000 08:17 3680626                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch_python.so
7f5ebfb94000-7f5ebfd93000 ---p 00802000 08:17 3680626                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch_python.so
7f5ebfd93000-7f5ebfda2000 r--p 00801000 08:17 3680626                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch_python.so
7f5ebfda2000-7f5ebfdbe000 rw-p 00810000 08:17 3680626                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch_python.so
7f5ebfdbe000-7f5ebfdfe000 rw-p 00000000 00:00 0
7f5ebfdfe000-7f5ebfeea000 rw-p 00a02000 08:17 3680626                    /usr/local/lib/python3.5/dist-packages/torch/lib/libtorch_python.so
7f5ebfeea000-7f5ebfef2000 r-xp 00000000 08:17 3680623                    /usr/local/lib/python3.5/dist-packages/torch/lib/libshm.so
7f5ebfef2000-7f5ec00f2000 ---p 00008000 08:17 3680623                    /usr/local/lib/python3.5/dist-packages/torch/lib/libshm.so
7f5ec00f2000-7f5ec00f3000 r--p 00008000 08:17 3680623                    /usr/local/lib/python3.5/dist-packages/torch/lib/libshm.so
7f5ec00f3000-7f5ec00f4000 rw-p 00009000 08:17 3680623                    /usr/local/lib/python3.5/dist-packages/torch/lib/libshm.so
7f5ec00f4000-7f5ec00f6000 rw-p 0000d000 08:17 3680623                    /usr/local/lib/python3.5/dist-packages/torch/lib/libshm.so
7f5ec00f6000-7f5ec00f8000 r-xp 00000000 08:17 3677065                    /usr/local/lib/python3.5/dist-packages/torch/_C.cpython-35m-x86_64-linux-gnu.so
7f5ec00f8000-7f5ec02f8000 ---p 00002000 08:17 3677065                    /usr/local/lib/python3.5/dist-packages/torch/_C.cpython-35m-x86_64-linux-gnu.so
7f5ec02f8000-7f5ec02f9000 r--p 00002000 08:17 3677065                    /usr/local/lib/python3.5/dist-packages/torch/_C.cpython-35m-x86_64-linux-gnu.so
7f5ec02f9000-7f5ec02fa000 rw-p 00003000 08:17 3677065                    /usr/local/lib/python3.5/dist-packages/torch/_C.cpython-35m-x86_64-linux-gnu.so
7f5ec02fa000-7f5ec02fb000 rw-p 00007000 08:17 3677065                    /usr/local/lib/python3.5/dist-packages/torch/_C.cpython-35m-x86_64-linux-gnu.so
7f5ec02fb000-7f5ec0338000 r-xp 00000000 08:17 4599167                    /usr/lib/x86_64-linux-gnu/libnvidia-fatbinaryloader.so.410.104
7f5ec0338000-7f5ec0538000 ---p 0003d000 08:17 4599167                    /usr/lib/x86_64-linux-gnu/libnvidia-fatbinaryloader.so.410.104
7f5ec0538000-7f5ec0543000 rw-p 0003d000 08:17 4599167                    /usr/lib/x86_64-linux-gnu/libnvidia-fatbinaryloader.so.410.104
7f5ec0543000-7f5ec0548000 rw-p 00000000 00:00 0
7f5ec0548000-7f5ec054f000 r-xp 00000000 08:17 2886956                    /lib/x86_64-linux-gnu/librt-2.23.so
7f5ec054f000-7f5ec074e000 ---p 00007000 08:17 2886956                    /lib/x86_64-linux-gnu/librt-2.23.so
7f5ec074e000-7f5ec074f000 r--p 00006000 08:17 2886956                    /lib/x86_64-linux-gnu/librt-2.23.so
7f5ec074f000-7f5ec0750000 rw-p 00007000 08:17 2886956                    /lib/x86_64-linux-gnu/librt-2.23.so
7f5ec0750000-7f5ec1b7a000 r-xp 00000000 08:17 3680619                    /usr/local/lib/python3.5/dist-packages/torch/lib/libnvrtc-007d19c9.so.9.0
7f5ec1b7a000-7f5ec1d79000 ---p 0142a000 08:17 3680619                    /usr/local/lib/python3.5/dist-packages/torch/lib/libnvrtc-007d19c9.so.9.0
7f5ec1d79000-7f5ec1f23000 rw-p 01429000 08:17 3680619                    /usr/local/lib/python3.5/dist-packages/torch/lib/libnvrtc-007d19c9.so.9.0
7f5ec1f23000-7f5ec1f9b000 rw-p 00000000 00:00 0
7f5ec1f9b000-7f5ec1f9d000 rw-p 015d3000 08:17 3680619                    /usr/local/lib/python3.5/dist-packages/torch/lib/libnvrtc-007d19c9.so.9.0
7f5ec1f9d000-7f5ec2d22000 r-xp 00000000 08:17 4463304                    /usr/lib/x86_64-linux-gnu/libcuda.so.410.104
7f5ec2d22000-7f5ec2f21000 ---p 00d85000 08:17 4463304                    /usr/lib/x86_64-linux-gnu/libcuda.so.410.104
7f5ec2f21000-7f5ec308f000 rw-p 00d84000 08:17 4463304                    /usr/lib/x86_64-linux-gnu/libcuda.so.410.104
7f5ec308f000-7f5ec309f000 rw-p 00000000 00:00 0
7f5ec309f000-7f5ec30a0000 r-xp 00000000 08:17 3677088                    /usr/local/lib/python3.5/dist-packages/torch/_nvrtc.cpython-35m-x86_64-linux-gnu.so
7f5ec30a0000-7f5ec329f000 ---p 00001000 08:17 3677088                    /usr/local/lib/python3.5/dist-packages/torch/_nvrtc.cpython-35m-x86_64-linux-gnu.so
7f5ec329f000-7f5ec32a0000 r--p 00000000 08:17 3677088                    /usr/local/lib/python3.5/dist-packages/torch/_nvrtc.cpython-35m-x86_64-linux-gnu.so
7f5ec32a0000-7f5ec32a1000 rw-p 00001000 08:17 3677088                    /usr/local/lib/python3.5/dist-packages/torch/_nvrtc.cpython-35m-x86_64-linux-gnu.so
7f5ec32a1000-7f5ec32a3000 rw-p 00006000 08:17 3677088                    /usr/local/lib/python3.5/dist-packages/torch/_nvrtc.cpython-35m-x86_64-linux-gnu.so
7f5ec32a3000-7f5ec32e3000 rw-p 00000000 00:00 0
7f5ec32e3000-7f5ec3305000 r-xp 00000000 08:17 3151829                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/nonproj.cpython-35m-x86_64-linux-gnu.so
7f5ec3305000-7f5ec3505000 ---p 00022000 08:17 3151829                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/nonproj.cpython-35m-x86_64-linux-gnu.so
7f5ec3505000-7f5ec3508000 rw-p 00022000 08:17 3151829                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/nonproj.cpython-35m-x86_64-linux-gnu.so
7f5ec3508000-7f5ec3526000 r-xp 00000000 08:17 3151831                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/transition_system.cpython-35m-x86_64-linux-gnu.so
7f5ec3526000-7f5ec3725000 ---p 0001e000 08:17 3151831                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/transition_system.cpython-35m-x86_64-linux-gnu.so
7f5ec3725000-7f5ec3728000 rw-p 0001d000 08:17 3151831                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/transition_system.cpython-35m-x86_64-linux-gnu.so
7f5ec3728000-7f5ec3737000 r-xp 00000000 08:17 3151834                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/stateclass.cpython-35m-x86_64-linux-gnu.so
7f5ec3737000-7f5ec3937000 ---p 0000f000 08:17 3151834                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/stateclass.cpython-35m-x86_64-linux-gnu.so
7f5ec3937000-7f5ec3939000 rw-p 0000f000 08:17 3151834                    /usr/local/lib/python3.5/dist-packages/spacy/syntax/stateclass.cpython-35m-x86_64-linux-gnu.so
7f5ec3939000-7f5ec396a000 r-xp 00000000 08:17 3149272                    /usr/local/lib/python3.5/dist-packages/thinc/linear/linear.cpython-35m-x86_64-linux-gnu.so
7f5ec396a000-7f5ec3b6a000 ---p 00031000 08:17 3149272                    /usr/local/lib/python3.5/dist-packages/thinc/linear/linear.cpython-35m-x86_64-linux-gnu.so
7f5ec3b6a000-7f5ec3b6e000 rw-p 00031000 08:17 3149272                    /usr/local/lib/python3.5/dist-packages/thinc/linear/linear.cpython-35m-x86_64-linux-gnu.so
7f5ec3b6e000-7f5ec3baf000 rw-p 00000000 00:00 0
7f5ec3baf000-7f5ec3bec000 r-xp 00000000 08:17 3149937                    /usr/local/lib/python3.5/dist-packages/spacy/vectors.cpython-35m-x86_64-linux-gnu.so
7f5ec3bec000-7f5ec3deb000 ---p 0003d000 08:17 3149937                    /usr/local/lib/python3.5/dist-packages/spacy/vectors.cpython-35m-x86_64-linux-gnu.so
7f5ec3deb000-7f5ec3df1000 rw-p 0003c000 08:17 3149937                    /usr/local/lib/python3.5/dist-packages/spacy/vectors.cpython-35m-x86_64-linux-gnu.so
7f5ec3df1000-7f5ec3e32000 rw-p 00000000 00:00 0
7f5ec3e32000-7f5ec3e55000 r-xp 00000000 08:17 3150605                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/_retokenize.cpython-35m-x86_64-linux-gnu.so
7f5ec3e55000-7f5ec4055000 ---p 00023000 08:17 3150605                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/_retokenize.cpython-35m-x86_64-linux-gnu.so
7f5ec4055000-7f5ec4058000 rw-p 00023000 08:17 3150605                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/_retokenize.cpython-35m-x86_64-linux-gnu.so
7f5ec4058000-7f5ec4098000 rw-p 00000000 00:00 0
7f5ec4098000-7f5ec40ad000 r-xp 00000000 08:17 3149924                    /usr/local/lib/python3.5/dist-packages/spacy/parts_of_speech.cpython-35m-x86_64-linux-gnu.so
7f5ec40ad000-7f5ec42ac000 ---p 00015000 08:17 3149924                    /usr/local/lib/python3.5/dist-packages/spacy/parts_of_speech.cpython-35m-x86_64-linux-gnu.so
7f5ec42ac000-7f5ec42af000 rw-p 00014000 08:17 3149924                    /usr/local/lib/python3.5/dist-packages/spacy/parts_of_speech.cpython-35m-x86_64-linux-gnu.so
7f5ec42af000-7f5ec42f5000 r-xp 00000000 08:17 3150609                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/token.cpython-35m-x86_64-linux-gnu.so
7f5ec42f5000-7f5ec44f5000 ---p 00046000 08:17 3150609                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/token.cpython-35m-x86_64-linux-gnu.so
7f5ec44f5000-7f5ec44fb000 rw-p 00046000 08:17 3150609                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/token.cpython-35m-x86_64-linux-gnu.so
7f5ec44fb000-7f5ec44fc000 rw-p 00000000 00:00 0
7f5ec44fc000-7f5ec4533000 r-xp 00000000 08:17 3150600                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/span.cpython-35m-x86_64-linux-gnu.so
7f5ec4533000-7f5ec4733000 ---p 00037000 08:17 3150600                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/span.cpython-35m-x86_64-linux-gnu.so
7f5ec4733000-7f5ec4738000 rw-p 00037000 08:17 3150600                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/span.cpython-35m-x86_64-linux-gnu.so
7f5ec4738000-7f5ec4739000 rw-p 00000000 00:00 0
7f5ec4739000-7f5ec4797000 r-xp 00000000 08:17 3150606                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/doc.cpython-35m-x86_64-linux-gnu.so
7f5ec4797000-7f5ec4997000 ---p 0005e000 08:17 3150606                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/doc.cpython-35m-x86_64-linux-gnu.so
7f5ec4997000-7f5ec499f000 rw-p 0005e000 08:17 3150606                    /usr/local/lib/python3.5/dist-packages/spacy/tokens/doc.cpython-35m-x86_64-linux-gnu.so
7f5ec499f000-7f5ec49e0000 rw-p 00000000 00:00 0
7f5ec49e0000-7f5ec4a14000 r-xp 00000000 08:17 3149918                    /usr/local/lib/python3.5/dist-packages/spacy/lexeme.cpython-35m-x86_64-linux-gnu.so
7f5ec4a14000-7f5ec4c13000 ---p 00034000 08:17 3149918                    /usr/local/lib/python3.5/dist-packages/spacy/lexeme.cpython-35m-x86_64-linux-gnu.so
7f5ec4c13000-7f5ec4c17000 rw-p 00033000 08:17 3149918                    /usr/local/lib/python3.5/dist-packages/spacy/lexeme.cpython-35m-x86_64-linux-gnu.so
7f5ec4c17000-7f5ec4c18000 rw-p 00000000 00:00 0
7f5ec4c18000-7f5ec4c57000 r-xp 00000000 08:17 3149920                    /usr/local/lib/python3.5/dist-packages/spacy/vocab.cpython-35m-x86_64-linux-gnu.so
7f5ec4c57000-7f5ec4e57000 ---p 0003f000 08:17 3149920                    /usr/local/lib/python3.5/dist-packages/spacy/vocab.cpython-35m-x86_64-linux-gnu.so
7f5ec4e57000-7f5ec4e5c000 rw-p 0003f000 08:17 3149920                    /usr/local/lib/python3.5/dist-packages/spacy/vocab.cpython-35m-x86_64-linux-gnu.so
7f5ec4e5c000-7f5ec4e5d000 rw-p 00000000 00:00 0
7f5ec4e5d000-7f5ec4e6f000 r-xp 00000000 08:17 3145798                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/testing.cpython-35m-x86_64-linux-gnu.so
7f5ec4e6f000-7f5ec506e000 ---p 00012000 08:17 3145798                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/testing.cpython-35m-x86_64-linux-gnu.so
7f5ec506e000-7f5ec5070000 rw-p 00011000 08:17 3145798                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/testing.cpython-35m-x86_64-linux-gnu.so
7f5ec5070000-7f5ec50b0000 rw-p 00000000 00:00 0
7f5ec50b0000-7f5ec50b1000 r-xp 00000000 08:17 3276939                    /usr/local/lib/python3.5/dist-packages/pandas/util/_move.cpython-35m-x86_64-linux-gnu.so
7f5ec50b1000-7f5ec52b1000 ---p 00001000 08:17 3276939                    /usr/local/lib/python3.5/dist-packages/pandas/util/_move.cpython-35m-x86_64-linux-gnu.so
7f5ec52b1000-7f5ec52b2000 rw-p 00001000 08:17 3276939                    /usr/local/lib/python3.5/dist-packages/pandas/util/_move.cpython-35m-x86_64-linux-gnu.so
7f5ec52b2000-7f5ec52c8000 r-xp 00000000 08:17 3146141                    /usr/local/lib/python3.5/dist-packages/pandas/io/msgpack/_unpacker.cpython-35m-x86_64-linux-gnu.so
7f5ec52c8000-7f5ec54c7000 ---p 00016000 08:17 3146141                    /usr/local/lib/python3.5/dist-packages/pandas/io/msgpack/_unpacker.cpython-35m-x86_64-linux-gnu.so
7f5ec54c7000-7f5ec54ca000 rw-p 00015000 08:17 3146141                    /usr/local/lib/python3.5/dist-packages/pandas/io/msgpack/_unpacker.cpython-35m-x86_64-linux-gnu.so
7f5ec54ca000-7f5ec54db000 r-xp 00000000 08:17 3146140                    /usr/local/lib/python3.5/dist-packages/pandas/io/msgpack/_packer.cpython-35m-x86_64-linux-gnu.so
7f5ec54db000-7f5ec56da000 ---p 00011000 08:17 3146140                    /usr/local/lib/python3.5/dist-packages/pandas/io/msgpack/_packer.cpython-35m-x86_64-linux-gnu.so
7f5ec56da000-7f5ec56dc000 rw-p 00010000 08:17 3146140                    /usr/local/lib/python3.5/dist-packages/pandas/io/msgpack/_packer.cpython-35m-x86_64-linux-gnu.so
7f5ec56dc000-7f5ec575c000 rw-p 00000000 00:00 0
7f5ec575c000-7f5ec578f000 r-xp 00000000 08:17 3145819                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/writers.cpython-35m-x86_64-linux-gnu.so
7f5ec578f000-7f5ec598f000 ---p 00033000 08:17 3145819                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/writers.cpython-35m-x86_64-linux-gnu.so
7f5ec598f000-7f5ec5993000 rw-p 00033000 08:17 3145819                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/writers.cpython-35m-x86_64-linux-gnu.so
7f5ec5993000-7f5ec5a14000 rw-p 00000000 00:00 0
7f5ec5a14000-7f5ec5a29000 r-xp 00000000 08:17 3145788                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/json.cpython-35m-x86_64-linux-gnu.so
7f5ec5a29000-7f5ec5c29000 ---p 00015000 08:17 3145788                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/json.cpython-35m-x86_64-linux-gnu.so
7f5ec5c29000-7f5ec5c2a000 rw-p 00015000 08:17 3145788                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/json.cpython-35m-x86_64-linux-gnu.so
7f5ec5c2a000-7f5ec5cae000 r-xp 00000000 08:17 3145792                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/parsers.cpython-35m-x86_64-linux-gnu.so
7f5ec5cae000-7f5ec5ead000 ---p 00084000 08:17 3145792                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/parsers.cpython-35m-x86_64-linux-gnu.so
7f5ec5ead000-7f5ec5eb4000 rw-p 00083000 08:17 3145792                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/parsers.cpython-35m-x86_64-linux-gnu.so
7f5ec5eb4000-7f5ec5f36000 rw-p 00000000 00:00 0
7f5ec5f36000-7f5ec5f4e000 r-xp 00000000 08:17 3145795                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/reshape.cpython-35m-x86_64-linux-gnu.so
7f5ec5f4e000-7f5ec614e000 ---p 00018000 08:17 3145795                    /usr/local/lib/python3.5/dist-packages/pandas/_libs/reshape.cpython-35m-x86_64-linux-gnu.soAborted (core dumped)
```
# model by filter ing supporting factors in the middle stage before self-attention:
reminder: i have already change the overall util function to include the extra is_support_word data structure. 
model for testing using only supporting facts:
    [model_test2](/model_test2.py)//
    [run_test2](/run_test2.py)//
    [util](/util.py)//
    [sp_model_test2](/sp_model_test2.py)//
training code:
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode train --para_limit 2250 --batch_size 12 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0
CUDA_VISIBLE_DEVICES=1 python main.py --mode train --para_limit 2250 --batch_size 12 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0
```
```
output for training:
-----------------------------------------------------------------------------------------
| eval     21 in epoch   2 | time: 869.02s | dev loss    3.625 | EM 48.4409 | F1 63.1520
-----------------------------------------------------------------------------------------
best_dev_F1 63.37813440065209
```
# model using only supporting factors
```
-----------------------------------------------------------------------------------------
| eval     15 in epoch   3 | time: 172.94s | dev loss    3.183 | EM 49.7772 | F1 64.5559
-----------------------------------------------------------------------------------------
best_dev_F1 64.60608215105948
```
```
{'em': 0.4973666441593518, 'f1': 0.6460608215105955,'prec': 0.6743275068393223, 'recall': 0.6661522409243548, 'sp_em': 0.0, 'sp_f1': 0.14916748942406766, 'sp_prec': 0.09017627499446443,'sp_recall': 0.45199430886466524,'joint_f1': 0.09847809921520946, 'joint_prec': 0.06095010805013573,'joint_recall': 0.3034137242643319, 'joint_em': 0.0}
```
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20190411-013304 --prediction_file dev_distractor_pred.json
```
```
python hotpot_evaluate_v1.py dev_distractor_pred.json hotpot_dev_distractor_v1.json
```
1. model for testing using only supporting facts:
    [model](/model_test1.py)
    [run](/run_test1.py)
# original file:
wordlength_csv file: [wordlength_csv](/length_vector.csv)
linux codes:
validation codes:
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20190329-013728 --prediction_file dev_distractor_pred.json
```
validation outputs:
```
| epoch   4 | step  17600 | lr 0.00156 | ms/batch 1139.40 | train loss    2.398
| epoch   4 | step  17700 | lr 0.00156 | ms/batch 1121.55 | train loss    2.487
| epoch   4 | step  17800 | lr 0.00156 | ms/batch 1114.87 | train loss    2.408
| epoch   4 | step  17900 | lr 0.00156 | ms/batch 1152.25 | train loss    2.371
| epoch   4 | step  18000 | lr 0.00156 | ms/batch 1154.26 | train loss    2.343
-----------------------------------------------------------------------------------------
| eval     18 in epoch   4 | time: 1292.35s | dev loss    4.860 | EM 42.5705 | F1 56.6056
-----------------------------------------------------------------------------------------
best_dev_F1 56.64527711671228
```
test commands:
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20190329-013728 --prediction_file dev_distractor_pred.json
```
```
python hotpot_evaluate_v1.py dev_distractor_pred.json hotpot_dev_distractor_v1.json
```
```
missing answer 5a87ab905542996e4f3088c1
missing sp fact 5a87ab905542996e4f3088c1
missing answer 5ab56e32554299637185c594
missing sp fact 5ab56e32554299637185c594
missing answer 5a760ab65542994ccc918697
missing sp fact 5a760ab65542994ccc918697
missing answer 5ab7f97a5542991d322237ef
missing sp fact 5ab7f97a5542991d322237ef
missing answer 5ab266b5554299340b5254b4
missing sp fact 5ab266b5554299340b5254b4
missing answer 5ae7eb3c5542994a481bbe20
missing sp fact 5ae7eb3c5542994a481bbe20

missing answer 5a8b595855429949d91db563
missing sp fact 5a8b595855429949d91db563
missing answer 5a80762a5542996402f6a536
missing sp fact 5a80762a5542996402f6a536
missing answer 5adbe2c65542996e68525274
missing sp fact 5adbe2c65542996e68525274
missing answer 5ab8f33155429919ba4e237f
missing sp fact 5ab8f33155429919ba4e237f
missing answer 5a8f495c5542997ba9cb3220
missing sp fact 5a8f495c5542997ba9cb3220
missing answer 5a753c8c55429916b01642ab
missing sp fact 5a753c8c55429916b01642ab
missing answer 5ae5be02554299546bf82f3e
missing sp fact 5ae5be02554299546bf82f3e
missing answer 5a9042825542990a984935d6
missing sp fact 5a9042825542990a984935d6
missing answer 5adfff0755429925eb1afbce
missing sp fact 5adfff0755429925eb1afbce
missing answer 5adfa22655429942ec259ac4
missing sp fact 5adfa22655429942ec259ac4
missing answer 5a8f541e5542992414482a53
missing sp fact 5a8f541e5542992414482a53
missing answer 5a8bf0835542995d1e6f146b
missing sp fact 5a8bf0835542995d1e6f146b
missing answer 5ae69e6d5542996d980e7c62
missing sp fact 5ae69e6d5542996d980e7c62
missing answer 5a808f3f5542992097ad2ffd
missing sp fact 5a808f3f5542992097ad2ffd
missing answer 5a7b68a75542997c3ec97153
missing sp fact 5a7b68a75542997c3ec97153
missing answer 5a722a6855429971e9dc9320
missing sp fact 5a722a6855429971e9dc9320
missing answer 5a8f122955429918e830d17f
missing sp fact 5a8f122955429918e830d17f
missing answer 5ab2f6bd554299166977415e
missing sp fact 5ab2f6bd554299166977415e
missing answer 5a74629255429929fddd8402
missing sp fact 5a74629255429929fddd8402
missing answer 5a85a37d5542997175ce1fe5
missing sp fact 5a85a37d5542997175ce1fe5
missing answer 5a87bd4e5542996432c57279
missing sp fact 5a87bd4e5542996432c57279
missing answer 5ae67fba5542996d980e7b9a
missing sp fact 5ae67fba5542996d980e7b9a
missing answer 5ab29426554299545a2cf99f
missing sp fact 5ab29426554299545a2cf99f
{'em': 0.42336259284267386,'f1': 0.5642343875933413,'prec': 0.5861020489751079,  'recall': 0.5826240661559602,  'sp_f1': 0.6191265655344054,'joint_prec': 0.3994076045306619, 'joint_em': 0.09020931802835921, 'joint_recall': 0.4101608971320206,  'sp_em': 0.17933828494260634, 'sp_recall': 0.6615560592906983, 'joint_f1': 0.37115038958007174, 'sp_prec': 0.6493791878464388}
```

# HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering

This repository contains the baseline model code, as well as the entire pipeline of running experiments on the HotpotQA dataset,
including data download, data preprocessing, training, and evaluation.

## Requirements

Python 3, pytorch 0.3.0, spacy

To install pytorch 0.3.0, follow the instructions at https://pytorch.org/get-started/previous-versions/ . For example, with
CUDA8 and conda you can do
```
conda install pytorch=0.3.0 cuda80 -c pytorch
```

To install spacy, run
```
conda install spacy
```

## Data Download and Preprocessing

Run the script to download the data, including HotpotQA data and GloVe embeddings, as well as spacy packages.
```
./download.sh
```

There are three HotpotQA files:
- Training set http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_train_v1.1.json
- Dev set in the distractor setting http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json
- Dev set in the fullwiki setting http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_fullwiki_v1.json This is just `hotpot_dev_distractor_v1.json` without the gold paragraphs, but instead with the top 10 paragraphs obtained using our
retrieval system. If you want to use your own IR system (which is encouraged!), you can replace the paragraphs in this json
with your own retrieval results. Please note that the gold paragraphs might or might not be in this json because our IR system
is pretty basic.
- Test set in the fullwiki setting http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_test_fullwiki_v1.json Because in the fullwiki setting, you only need to submit your prediction to our evaluation server without the code, we publish the test set without the answers and supporting facts. The context in the file is paragraphs obtained using our retrieval system, which might or might not contain the gold paragraphs. Again you are encouraged to use your own IR system in this setting --- simply replace the paragraphs in this json with your own retrieval results.


## JSON Format

The top level structure of each JSON file is a list, where each entry represents a question-answer data point. Each data point is
a dict with the following keys:
- `_id`: a unique id for this question-answer data point. This is useful for evaluation.
- `question`: a string.
- `answer`: a string. The test set does not have this key.
- `supporting_facts`: a list. Each entry in the list is a list with two elements `[title, sent_id]`, where `title` denotes the title of the 
paragraph, and `sent_id` denotes the supporting fact's id (0-based) in this paragraph. The test set does not have this key.
- `context`: a list. Each entry is a paragraph, which is represented as a list with two elements `[title, sentences]` and `sentences` is a list
of strings.

There are other keys that are not used in our code, but might be used for other purposes (note that these keys are not present in the test sets, and your model should not rely on these two keys for making preditions on the test sets):
- `type`: either `comparison` or `bridge`, indicating the question type. (See our paper for more details).
- `level`: one of `easy`, `medium`, and `hard`. (See our paper for more details).

## Preprocessing

Preprocess the training and dev sets in the distractor setting:
```
python main.py --mode prepro --data_file hotpot_train_v1.1.json --para_limit 2250 --data_split train
python main.py --mode prepro --data_file hotpot_dev_distractor_v1.json --para_limit 2250 --data_split dev
```

Preprocess the dev set in the full wiki setting:
```
python main.py --mode prepro --data_file hotpot_dev_fullwiki_v1.json --data_split dev --fullwiki --para_limit 2250
```

Note that the training set has to be preprocessed before the dev sets because some vocabulary and embedding files are produced
when the training set is processed.

## Training

Train a model
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode train --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0
```

Our implementation supports running on multiple GPUs. Remove the `CUDA_VISIBLE_DEVICES` variable to run on all GPUs you have
```
python main.py --mode train --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0
```

You will be able to see the perf reach over 58 F1 on the dev set. Record the file name (something like `HOTPOT-20180924-160521`)
which will be used during evaluation.

## Local Evaluation

First, make predictions and save the predictions into a file (replace `--save` with your own file name).
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20180924-160521 --prediction_file dev_distractor_pred.json
```

Then, call the evaluation script:
```
python hotpot_evaluate_v1.py dev_distractor_pred.json hotpot_dev_distractor_v1.json
```

The same procedure can be repeated to evaluate the dev set in the fullwiki setting.
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20180924-160521 --prediction_file dev_fullwiki_pred.json --fullwiki python hotpot_evaluate_v1.py dev_fullwiki_pred.json hotpot_dev_fullwiki_v1.json
```

## Prediction File Format

The prediction files `dev_distractor_pred.json` and `dev_fullwiki_pred.json` should be JSON files with the following keys:
- `answer`: a dict. Each key of the dict is a QA pair id, corresponding to the field `_id` in data JSON files. Each value of the dict is a string representing the predicted answer.
- `sp`: a dict. Each key of the dict is a QA pair id, corresponding to the field `_id` in data JSON files. Each value of the dict is a list representing the predicted supporting facts. Each entry of the list is a list with two elements `[title, sent_id]`, where `title` denotes the title of the paragraph, and `sent_id` denotes the supporting fact's id (0-based) in this paragraph.

## Model Submission and Test Set Evaluation

We use Codalab for test set evaluation. In the distractor setting, you must submit your code and provide a Docker environment. Your code will run on the test set. In the fullwiki setting, you only need to submit your prediction file. See https://worksheets.codalab.org/worksheets/0xa8718c1a5e9e470e84a7d5fb3ab1dde2/ for detailed instructions.

## License
The HotpotQA dataset is distribued under the [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/legalcode) license.
The code is distribued under the Apache 2.0 license.

## References

The preprocessing part and the data loader are adapted from https://github.com/HKUST-KnowComp/R-Net . The evaluation script is
adapted from https://rajpurkar.github.io/SQuAD-explorer/ .



