**Added:**

* New fixie credential credentialing service that allows users to request service
  tokens associated with a user name and an email address. The service token itself
  never stored on the server. Instead, the hash of the token is stored on the server.
  The user is responsible for storing and managing the token once they recieve it.
  Service tokens can be reset with the original name/email address pair. User may
  also deregister themselves with a working token.

**Changed:** None

**Deprecated:** None

**Removed:** None

**Fixed:** None

**Security:** None
