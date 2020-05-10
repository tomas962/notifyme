
from pywebpush import webpush
import json

webpush({"endpoint":"https://fcm.googleapis.com/fcm/send/dJpkfE3_ajw:APA91bEWvEBB0x6f_qAaCxNt3G4aBbdzT-usH1K_1HtIo6cjmYiTrDHB1B6SxFbwE2JU_VL_ykgOvivljAihLDln3_qYnXBJIC5UqviHDv6t76PgodtfYBG_P-JEe1cKLjs1fqTfcJMf","expirationTime":None,"keys":{"p256dh":"BPF4_pI-nhkbiqkej8air6L_miVCpdBifu-jWJrQlGkLxMGhL9tgNCBxrQbwuxP2rcA5inNrOdX_VETtwTlLHl0","auth":"jUMP_NXfGyY_7zB8PPTM2Q"}}, 
         data=json.dumps({"title":"My title", "body":"My blooolody"}), 
         vapid_private_key='./vapid_private.pem', vapid_claims={"sub":"mailto:cctomass@gmail.com"}, verbose=True)
