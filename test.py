from cryptobox.cbox import CBox, CBoxVec
import base64
# cipher_raw = "owABAaEAWCBY172OsoLvMH8E9qqbg6pSr76jVD8OO5qfvnGSpkhlvgJYkQGlAFBOr8sN9Fe2+5UpA92UjnT5AQACAAOhAFggI6aIEgo05d26smW22JwuhGdpuSzeN2onMXbnAFwcc3AEWFFC6AZ2dMBo79NA+iv+EAsy1kpoNc/7bzRjJieaMaWZkAJPSSG3iTbT8BzuGrXVJKeH9z7Bnw3IKyG/Tg6sdIEcApQNjbY/cf2Opewjvt+HwSE="
cipher_raw = "owABAaEAWCD+B1ZxBXywZtPCxr+kmgltdfTiRhXgvGnpJEzJ+AaWawJYkQGlAFBOr8sN9Fe2+5UpA92UjnT5AQACAgOhAFgg3hUP7HU54UVcBCfR9vV1yqHxGtHzJjKpsVvUQjw3nssEWFEHHVcA6hyknkEEqL3SvbZUljq+C94tdFzpqRP0Z5bV0Tspu+wVBMO/poRue3mZZp2FuXpYX3bRnTcgtuCYFRukrkolFlhMe5yInf/LfDZ1rYE="
cipher = base64.standard_b64decode(cipher_raw)

c = CBox()
c.file_open("box")
c.new_pre_keys(42)
c.session_from_message("hello", cipher)

vec = CBoxVec()
print(vec.len())

c.close()
