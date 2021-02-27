using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EyeBall : MonoBehaviour
{
    void Update () 
    {
        // Eyecontact
        transform.LookAt(Camera.main.ScreenToWorldPoint(Input.mousePosition));
    }
}
