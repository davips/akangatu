# from akangatu.mixin.operators import withOperators
# from akangatu.mixin.sampling import withSampling
# from transf.transformer import Transformer
#
#
# class Inner(Transformer, withSampling, withOperators):
#     def __init__(self, transformer):
#         self.transformer=transformer
#
#     def _core_transform_(self, data):
#         newinner = self.transformer.transform(data.inner)
#
#     def _config_(self):
#         pass